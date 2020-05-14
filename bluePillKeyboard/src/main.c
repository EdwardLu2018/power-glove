/*
 * Turns an STM32F103 device into an HID keyboard and mouse
 */
#include <stdlib.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/usb/usbd.h>
#include <libopencm3/usb/hid.h>

#include "delay.h"
#include "hid.h"
#include "mouse.h"
#include "keyboard.h"

static usbd_device *usbd_dev;

static const char *usb_strings[] = {
    "Build18 Technologies",
    "Power Glove"
};

const struct usb_interface ifaces[] = {{
    .num_altsetting = 1,
    .altsetting = &hid_iface
}};

const struct usb_config_descriptor config = {
    .bLength = USB_DT_CONFIGURATION_SIZE,
    .bDescriptorType = USB_DT_CONFIGURATION,
    .wTotalLength = 0,
    .bNumInterfaces = 1,
    .bConfigurationValue = 1,
    .iConfiguration = 0,
    .bmAttributes = 0xC0,
    .bMaxPower = 0x32,

    .interface = ifaces,
};

const struct usb_device_descriptor dev_descr = {
    .bLength = USB_DT_DEVICE_SIZE,
    .bDescriptorType = USB_DT_DEVICE,
    .bcdUSB = 0x0200,
    .bDeviceClass = 0,
    .bDeviceSubClass = 0,
    .bDeviceProtocol = 0,
    .bMaxPacketSize0 = 64,
    .idVendor = 0x05ac,     // set vendor to Apple Inc to get rid of keyboard verification on macs
    .idProduct = 0x2227,    // same as above
    .bcdDevice = 0x0200,
    .iManufacturer = 1,
    .iProduct = 2,
    .iSerialNumber = 3,
    .bNumConfigurations = 1,
};

static void setup_rcc(void) {
    rcc_clock_setup_in_hsi_out_48mhz();
    rcc_periph_clock_enable(RCC_GPIOC);

    rcc_periph_clock_enable(RCC_GPIOA);
    rcc_periph_clock_enable(RCC_USART2);
}

static void setup_serial(void) {
    nvic_enable_irq(NVIC_USART2_IRQ);

    gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_50_MHZ, GPIO_CNF_OUTPUT_ALTFN_PUSHPULL, GPIO_USART2_TX);
    gpio_set_mode(GPIOA, GPIO_MODE_INPUT, GPIO_CNF_INPUT_FLOAT, GPIO_USART2_RX);

    usart_set_baudrate(USART2, 9600);
    usart_set_databits(USART2, 8);
    usart_set_stopbits(USART2, USART_STOPBITS_1);
    usart_set_mode(USART2, USART_MODE_TX_RX);
    usart_set_parity(USART2, USART_PARITY_NONE);
    usart_set_flow_control(USART2, USART_FLOWCONTROL_NONE);

    USART_CR1(USART2) |= USART_CR1_RXNEIE;

    usart_enable(USART2);
}

static void setup_led(void) {
    gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
    gpio_set(GPIOC, GPIO13);
}

/* Buffer to be used for control requests. */
uint8_t usbd_control_buffer[128];

int main(void) {
    setup_rcc();
    setup_serial();
    setup_led();
    setup_delay();

	usbd_dev = usbd_init(&st_usbfs_v1_usb_driver, &dev_descr, &config,
						 usb_strings, sizeof(usb_strings)/sizeof(char *),
						 usbd_control_buffer, sizeof(usbd_control_buffer));
	usbd_register_set_config_callback(usbd_dev, hid_set_config);

	while (0 == 0)
		usbd_poll(usbd_dev);
}

static uint16_t mouse_click(uint8_t type) {
	uint8_t report[5] = {0};
    report[0] = MOUSE_REPORT_ID;
    report[1] = type;
	return usbd_ep_write_packet(usbd_dev, 0x81, &report, sizeof(report));
}

static uint16_t mouse_move_x_by(uint8_t by) {
	uint8_t report[5] = {0};
    report[0] = MOUSE_REPORT_ID;
    report[2] = by;
	return usbd_ep_write_packet(usbd_dev, 0x81, &report, sizeof(report));
}

static uint16_t mouse_move_y_by(uint8_t by) {
	uint8_t report[5] = {0};
    report[0] = MOUSE_REPORT_ID;
    report[3] = by;
	return usbd_ep_write_packet(usbd_dev, 0x81, &report, sizeof(report));
}

static uint16_t mouse_scroll(uint8_t by) {
	uint8_t report[5] = {0};
    report[0] = MOUSE_REPORT_ID;
    report[4] = by;
	return usbd_ep_write_packet(usbd_dev, 0x81, &report, sizeof(report));
}

static uint16_t keyboard_press(uint8_t key) {
    // report id, modifiers, reserved, keys[6], leds
	uint8_t report[9] = {0};
	report[0] = KEYBOARD_REPORT_ID;
	report[1] = 0;
	report[2] = 1;
    report[3] = key;
	return usbd_ep_write_packet(usbd_dev, 0x81, &report, sizeof(report));
}

static uint8_t keys_buf[256] = {0};
static uint8_t keys_len = 0;
static uint8_t key_idx = 0;
static void keyboard_tap(uint8_t key) {
    if (keys_len >= 256) {
        keys_len = 0;
        key_idx = 0;
    }
    keys_buf[keys_len] = key;
    ++keys_len;
    keys_buf[keys_len] = KEY_NONE;
    ++keys_len;
}

volatile uint8_t recved = 0;
volatile uint64_t system_millis = 0;
void sys_tick_handler(void) {
    static uint8_t numlock_flag = 1;
    if (numlock_flag) {
        keyboard_tap(KEY_NUMLOCK);
        numlock_flag = 0;
    }

    // blink on-board led as a sanity check that system is on
    if (system_millis % 500 == 0) {
        gpio_toggle(GPIOC, GPIO13);
    }

    // test that it can send 'a' without spamming
    // if (system_millis % 1000 == 0) {
    //     keyboard_tap(KEY_A);
    // }

    // loop to send current key to tap and then release, must be done in 2 cycles
    // for some reason
    if (system_millis % 100 == 0 && key_idx < keys_len) {
        keyboard_press(keys_buf[key_idx]);
        ++key_idx;
    }

	++system_millis;
}

void usart2_isr(void) {

    /* Check if we were called because of RXNE */
    if (((USART_CR1(USART2) & USART_CR1_RXNEIE) != 0) &&
        ((USART_SR(USART2) & USART_SR_RXNE) != 0)) {

        // gpio_toggle(GPIOC, GPIO13);

        recved = usart_recv(USART2);
        switch (recved) {
            case 'h':
                keyboard_tap(KEY_H);
                break;
            case 'i':
                keyboard_tap(KEY_I);
                break;
            case 't':
                keyboard_press(KEY_T);
                delay_us(-1);
                keyboard_press(KEY_NONE);
                delay_us(-1);
                break;
            case 'w':
                mouse_move_y_by(-5);
                break;
            case 'a':
                mouse_move_x_by(-5);
                break;
            case 's':
                mouse_move_y_by(5);
                break;
            case 'd':
                mouse_move_x_by(5);
                break;
            default:
                break;
        }

        /* Enable transmit interrupt */
        USART_CR1(USART2) |= USART_CR1_TXEIE;
    }

    /* Check if we were called because of TXE */
    if (((USART_CR1(USART2) & USART_CR1_TXEIE) != 0) &&
        ((USART_SR(USART2) & USART_SR_TXE) != 0)) {

        // gpio_toggle(GPIOC, GPIO13);

        usart_send(USART2, recved);

        /* Disable the TXE interrupt */
        USART_CR1(USART2) &= ~USART_CR1_TXEIE;

        recved = KEY_NONE;
    }
}
