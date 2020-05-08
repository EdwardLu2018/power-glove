#include <stdlib.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/usb/usbd.h>
#include <libopencm3/usb/hid.h>
#include "hid.h"

static usbd_device *usbd_dev;

static const char *usb_strings[] = {
    "Build18 Technologies",
    "Power Glove"
};

/* Buffer to be used for control requests. */
uint8_t usbd_control_buffer[128];

static void hid_set_config(usbd_device *dev, uint16_t wValue) {
	(void)wValue;
	(void)dev;

	usbd_ep_setup(dev, 0x81, USB_ENDPOINT_ATTR_INTERRUPT, 4, NULL);

	usbd_register_control_callback(
				dev,
				USB_REQ_TYPE_STANDARD | USB_REQ_TYPE_INTERFACE,
				USB_REQ_TYPE_TYPE | USB_REQ_TYPE_RECIPIENT,
				hid_control_request);

	systick_set_clocksource(STK_CSR_CLKSOURCE_AHB_DIV8);
	systick_set_reload(8999); // 1 ms
	systick_interrupt_enable();
	systick_counter_enable();
}

int main(void) {
	rcc_clock_setup_in_hsi_out_48mhz();
	rcc_periph_clock_enable(RCC_GPIOC);

	gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ,
		GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
	gpio_set(GPIOC, GPIO13);

	usbd_dev = usbd_init(&st_usbfs_v1_usb_driver, &dev_descr, &config,
						 usb_strings, 3,
						 usbd_control_buffer, sizeof(usbd_control_buffer));
	usbd_register_set_config_callback(usbd_dev, hid_set_config);

	while (1)
		usbd_poll(usbd_dev);
}

void sys_tick_handler(void) {
	static int x = 0;
	static int dir = 1;
	uint8_t buf[4] = {0, 0, 0, 0};

	//     Byte | D7      D6      D5      D4      D3      D2      D1      D0
 	//    ------+---------------------------------------------------------------------
 	//      0   |  0       0       0    Forward  Back    Middle  Right   Left (Button)
 	//      1   |                             X
 	//      2   |                             Y
 	//      3   |                       Vertical Wheel

	buf[1] = dir;
	x += dir;
	if (x > 30)
		dir = -dir;
	if (x < -30)
		dir = -dir;

	usbd_ep_write_packet(usbd_dev, 0x81, buf, 4);
}
