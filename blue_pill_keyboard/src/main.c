#include <stdlib.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/usb/usbd.h>
#include <libopencm3/usb/hid.h>

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

/* Buffer to be used for control requests. */
uint8_t usbd_control_buffer[128];

int main(void) {
	rcc_clock_setup_in_hsi_out_48mhz();
	rcc_periph_clock_enable(RCC_GPIOC);

	gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ,
		GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
	gpio_set(GPIOC, GPIO13);

	usbd_dev = usbd_init(&st_usbfs_v1_usb_driver, &dev_descr, &config,
						 usb_strings, sizeof(usb_strings)/sizeof(char *),
						 usbd_control_buffer, sizeof(usbd_control_buffer));
	usbd_register_set_config_callback(usbd_dev, hid_set_config);

	while (1)
		usbd_poll(usbd_dev);
}

static uint16_t mouse_move_x_by(uint8_t by) {
	uint8_t buf[5] = {MOUSE_REPORT_ID, 0, by, 0, 0};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 5);
}

static uint16_t mouse_move_y_by(uint8_t by) {
	uint8_t buf[5] = {MOUSE_REPORT_ID, 0, 0, by, 0};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 5);
}

static uint16_t mouse_click(uint8_t type) {
	uint8_t buf[5] = {MOUSE_REPORT_ID, type, 0, 0, 0};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 5);
}

static uint16_t mouse_scroll(uint8_t by) {
	uint8_t buf[5] = {MOUSE_REPORT_ID, 0, 0, 0, by};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 5);
}

static uint16_t keyboard_press(uint8_t character) {
	uint8_t buf[10] = {KEYBOARD_REPORT_ID, 0, 1, character, 0, 0, 0, 0, 0, 0};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 10);
}

static uint16_t keyboard_release() {
	uint8_t buf[10] = {KEYBOARD_REPORT_ID, 0, 1, KEY_NONE, 0, 0, 0, 0, 0, 0};
	return usbd_ep_write_packet(usbd_dev, 0x81, buf, 10);
}

void sys_tick_handler(void) {
	// static int x = 0;
	// static int by = 1;
	// x += by;
	// if (x > 100)
	// 	by = -by;
	// if (x < -100)
	// 	by = -by;
	// mouse_move_by(by);

	// mouse_scroll(-5);

	mouse_click(LEFT_CLICK);
	for (int i = 0; i < 10000; i++) __asm__("nop");
	mouse_click(0x0);

	// keyboard_press(KEY_A);
	// for (int i=0; i < 100000; i++);
	// keyboard_release();

	gpio_toggle(GPIOC, GPIO13);
}
