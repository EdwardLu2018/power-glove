#include <stdlib.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/usart.h>
#include <libopencm3/cm3/nvic.h>
#include <libopencm3/cm3/systick.h>

static void setup_rcc(void) {
    rcc_clock_setup_in_hsi_out_48mhz();

    rcc_periph_clock_enable(RCC_GPIOC);

    rcc_periph_clock_enable(RCC_GPIOA);
    rcc_periph_clock_enable(RCC_USART1);
}

static void setup_serial(void) {
    gpio_set_mode(GPIOA, GPIO_MODE_OUTPUT_50_MHZ, GPIO_CNF_OUTPUT_ALTFN_PUSHPULL, GPIO_USART1_TX);

    usart_set_baudrate(USART1, 9600);
    usart_set_databits(USART1, 8);
    usart_set_stopbits(USART1, USART_STOPBITS_1);
    usart_set_mode(USART1, USART_MODE_TX | USART_MODE_RX);
    usart_set_parity(USART1, USART_PARITY_NONE);
    usart_set_flow_control(USART1, USART_FLOWCONTROL_NONE);

    usart_enable(USART1);
}

static void setup_led(void) {
    gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
}

static void setup_systick(void) {
    systick_set_clocksource(STK_CSR_CLKSOURCE_AHB_DIV8);
    systick_set_reload(8999); // 1 ms
    systick_interrupt_enable();
    systick_counter_enable();
}

int main(void) {
    setup_rcc();
    setup_serial();
    setup_led();
    setup_systick();

    while(1) {}
}

volatile uint32_t system_millis = 0;
void sys_tick_handler(void) {
    if (++system_millis % 100 == 0) {
        if (usart_recv_blocking(USART1) == '0') {
            gpio_toggle(GPIOC, GPIO13);
            usart_send_blocking(USART1, 'a');
        }
        // delay
        for (size_t i = 0; i < 800000; i++)
            __asm__("NOP");
    }
}
