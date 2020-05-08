ifneq ($(V), 1)
MAKEFLAGS += --no-print-dir
Q := @
endif

BINARY = pg_hid

OPT_FLAGS ?= -O2

CFLAGS += -Wall -Wextra -Werror -Wno-char-subscripts\
	$(OPT_FLAGS) -std=gnu99 -g3 -MD \
	-I.
LDFLAGS += $(OPT_FLAGS)

C_SOURCES = $(shell find . -name "*.c")

CROSS_COMPILE ?= arm-none-eabi-
CC = $(CROSS_COMPILE)gcc
OBJCOPY = $(CROSS_COMPILE)objcopy

OPT_FLAGS = -Os
CFLAGS += -mcpu=cortex-m3 -mthumb \
	-DSTM32F1 -DDISCOVERY_STLINK -I../libopencm3/include \
	-I .
LDFLAGS_BOOT := $(LDFLAGS) --specs=nano.specs \
	-lopencm3_stm32f1 -Wl,--defsym,_stack=0x20005000 \
	-Wl,-T,$(BINARY).ld -nostartfiles -lc \
	-mthumb -mcpu=cortex-m3 -Wl,-gc-sections \
	-L../libopencm3/lib
LDFLAGS = $(LDFLAGS_BOOT)

LDFLAGS += --specs=nosys.specs

all:	$(BINARY).bin

host_clean:
	-$(Q)$(RM) $(BINARY).bin

OBJ = $(C_SOURCES:.c=.o)

$(BINARY).elf: $(OBJ)
	@echo "  LD      $@"
	$(Q)$(CC) -o $@ $(OBJ) $(LDFLAGS)

%.o:	%.c
	@echo "  CC      $<"
	$(Q)$(CC) $(CFLAGS) -c $< -o $@

%.bin:	%.elf
	@echo "  OBJCOPY $@"
	$(Q)$(OBJCOPY) -O binary $^ $@

%.hex:	%
	@echo "  OBJCOPY $@"
	$(Q)$(OBJCOPY) -O ihex $^ $@

.PHONY:	clean host_clean FORCE

clean:	host_clean
	-$(Q)$(RM) -f *.o *.d *~ *.elf *.bin $(HOSTFILES)

openocd:
	openocd -f openocd.cfg

telnet:
	telnet localhost 4444

gdb: $(BINARY).elf
	arm-none-eabi-gdb --eval-command="target remote localhost:3333" $<

-include *.d
