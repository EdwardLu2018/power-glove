#ifndef MOUSE_H
#define MOUSE_H

/* MOUSE USAGE:
 * Byte | D7      D6      D5      D4      D3      D2      D1      D0
 * -------------------------------------------------------------------
 *   0  |  0       0       0    Forward  Back    Middle  Right   Left (Button)
 *   1  |                             X
 *   2  |                             Y
 *   3  |                       Vertical Wheel
 */

#define LEFT_CLICK      (0x01)
#define RIGHT_CLICK     (0b10)
#define MIDDLE_CLICK    (0b10)
#define FORWARD         (0b100)
#define BACKWARD        (0b1000)

#endif
