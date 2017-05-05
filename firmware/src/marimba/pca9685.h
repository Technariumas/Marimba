/**
 ******************************************************************************
 * @file	pca9685.h
 * @author	Hampus Sandberg
 * @version	0.1
 * @date	2013-04-04
 * @brief	Contains function prototypes to manage the PCA9685 LED Driver
 ******************************************************************************
 */

#include <avr/io.h>
#include "twi.h"

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef PCA9685_H_
#define PCA9685_H_

/* Includes ------------------------------------------------------------------*/
/* Defines -------------------------------------------------------------------*/

/* Typedefs ------------------------------------------------------------------*/
/**
 * @brief	PCA9685 Inverted outputs
 */
typedef enum
{
	PCA9685_NotInvOutputs =	0,
	PCA9685_InvOutputs =	1
} PCA9685_InvOutputs_TypeDef;
#define IS_PCA9685_INV_OUTPUTS(INVRT)	(((INVRT) == PCA9685_NotInvOutputs) || \
										((INVRT) == PCA9685_InvOutputs))

/**
 * @brief  PCA9685 Output driver types
 */
typedef enum
{
	PCA9685_OutputDriver_OpenDrain =	0,
	PCA9685_OutputDriver_TotemPole =	1
} PCA9685_OutputDriver_TypeDef;
#define IS_PCA9685_OUTPUT_DRIVER(OUTPUT_DRIVER)	(((OUTPUT_DRIVER) == PCA9685_OutputDriver_OpenDrain) || \
												((OUTPUT_DRIVER) == PCA9685_OutputDriver_TotemPole))

/**
 * @brief	PCA9685 Not enabled LED outputs defines the behaviour of the outputs
 *			when OE is pulled low
 */
typedef enum
{
	PCA9685_OutputNotEn_0 =			0,
	PCA9685_OutputNotEn_OUTDRV =	1,
	PCA9685_OutputNotEn_High_Z1 =	2,
	PCA9685_OutputNotEn_High_Z2 =	3
} PCA9685_OutputNotEn_TypeDef;
#define IS_PCA9685_OUTPUT_NOT_EN(OUTNE)	(((OUTNE) >= PCA9685_OutputNotEn_0) && \
										((OUTNE) <= PCA9685_OutputNotEn_High_Z2))
										
/**
 * @brief	PCA9685 Frequency
 *			Set by prescale = round(25 MHz / (4096 * freq)) - 1
 */
typedef enum
{
	PCA9685_Frequency_200Hz =	30,
	PCA9685_Frequency_100Hz =	60,
	PCA9685_Frequency_60Hz =	100,
	PCA9685_Frequency_50Hz =	121
} PCA9685_Frequency;
#define IS_PCA9685_FREQUENCY(FREQ) ((FREQ) == PCA9685_Frequency_200Hz || \
									(FREQ) == PCA9685_Frequency_100Hz || \
									(FREQ) == PCA9685_Frequency_60Hz || \
									(FREQ) == PCA9685_Frequency_50Hz)

/**
 * @brief	PCA9685 Init structure definition
 */
typedef struct
{
    uint8_t Address;							/** Specifies the address for the PCA9685 */
    PCA9685_InvOutputs_TypeDef InvOutputs;		/** Specifies if the outputs should be inverted
    												This parameter can be any value of PCA9685_InvOutputs_TypeDef */
    PCA9685_OutputDriver_TypeDef OutputDriver;	/** Specifies the output driver 
    												This parameter can be any value of PCA9685_OutputDriver_TypeDef */
	PCA9685_OutputNotEn_TypeDef OutputNotEn;	/** Specifies what the outputs should be when OE=1
    												This parameter can be any value of PCA9685_OutputNotEn_TypeDef */
	PCA9685_Frequency PWMFrequency;				/** Specifies what output frequency to use
    												This parameter can be any value of PCA9685_Frequency */
} PCA9685_Init_TypeDef;


/* Function prototypes -------------------------------------------------------*/
uint8_t PCA9685_Init(PCA9685_Init_TypeDef *PCA9685_InitStruct);
uint8_t PCA9685_Init2();
void PCA9685_SetOutput(uint8_t Address, uint8_t Output, uint16_t OffValue);


/* Private defines -----------------------------------------------------------*/
#define MODE1				0x00
	#define MODE1_ALLCALL	0
	#define MODE1_SUB3		1
	#define MODE1_SUB2		2
	#define MODE1_SUB1		3
	#define MODE1_SLEEP		4
	#define MODE1_AI		5
	#define MODE1_EXTCLK	6
	#define MODE1_RESTART	7

#define MODE2				0x01
	#define MODE2_OUTNE0	0
	#define MODE2_OUTNE1	1
	#define MODE2_OUTDRV	2
	#define MODE2_OCH		3
	#define MODE2_INVRT		4

#define SUBADR1				0x02
#define SUBADR2				0x03
#define SUBADR3				0x04
#define ALLCALLADR			0x05

#define LEDn_ON_L(n)		(0x06 + (n)*4)
#define LEDn_ON_H(n)		(0x07 + (n)*4)
#define LEDn_OFF_L(n)		(0x08 + (n)*4)
#define LEDn_OFF_H(n)		(0x09 + (n)*4)

#define ALL_LED_ON_L		0xFA
#define ALL_LED_ON_H		0xFB
#define ALL_LED_OFF_L		0xFC
#define ALL_LED_OFF_H		0xFD

#define PRE_SCALE			0xFE

#define MAX_OUTPUT_INDEX	15
#define MAX_OUTPUT_VALUE	0xFFF

/* Private variables ---------------------------------------------------------*/
/* Private functions ---------------------------------------------------------*/
/* Functions -----------------------------------------------------------------*/

/**
 * @brief	Initializes the PCA9685
 * @param	None
 * @retval	1: A PCA9685 at address [Address] has been initialized
 * @retval	0: Initialization failed
 */
void PCA9685_Init() {
	TWI_InitStandard();
	
	// if (TWI_SlaveAtAddress(PCA9685_InitStruct->Address))
	// {

		// TWI_BeginTransmission(PCA9685_InitStruct->Address);
		// TWI_Write(MODE1);
		// TWI_Write(0);
		// TWI_EndTransmission();

		// uint8_t mode1 = 0;
		// TWI_RequestFrom(PCA9685_InitStruct->Address, &mode1, 1);
		
		// TWI_BeginTransmission(PCA9685_InitStruct->Address);
		// TWI_Write(MODE1);
		// TWI_Write(0x10);
		// TWI_EndTransmission();

		TWI_BeginTransmission(0x40);
		TWI_Write(PRE_SCALE);
		TWI_Write(3);//
		TWI_EndTransmission();

		delayMicroseconds(600);
		TWI_BeginTransmission(0x40);
		TWI_Write(MODE1);
		TWI_Write((1 << MODE1_AI));//0xA1
		TWI_EndTransmission();
		
		/* MODE2 Register:
		 * Outputs change on STOP command
		 */
		// uint8_t mode2 = (PCA9685_InitStruct->InvOutputs << MODE2_INVRT) |
		// (PCA9685_InitStruct->OutputDriver << MODE2_OUTDRV) |
		// (PCA9685_InitStruct->OutputNotEn << MODE2_OUTNE0);
		// TWI_BeginTransmission(PCA9685_InitStruct->Address);
		// TWI_Write(MODE2);
		// TWI_Write(mode2);
		// TWI_EndTransmission();
		
		
		// // TESTING - 50% Duty. On at 0 and off at 2047 (0x7FF)
		// TWI_BeginTransmission(PCA9685_InitStruct->Address);
		// TWI_Write(LEDn_ON_L(1));
		// TWI_Write(0x00);	// ALL_LED_ON_L
 	// 	TWI_Write(0x00);	// ALL_LED_ON_H
 	// 	TWI_Write(0xFF);	// ALL_LED_OFF_L
 	// 	TWI_Write(0x07);	// ALL_LED_OFF_H
		// TWI_EndTransmission();
		
		// PCA9685_SetOutput(PCA9685_InitStruct->Address, 1, 2050);

		// TWI_BeginTransmission(PCA9685_InitStruct->Address);
		// TWI_Write(LEDn_ON_L(1));
		// TWI_EndTransmission();
		// volatile uint8_t data[4] = {};
		// twiStatus = TWI_RequestFrom(PCA9685_InitStruct->Address, data, 4);
		// volatile uint8_t test = 0;
 	// }
}

/**
 * @brief	Sets a specific output for a PCA9685
 * @param	Address: The address to the PCA9685
 * @param	Output: The output to set
 * @param	OnValue: The value at which the output will turn on
 * @param	OffValue: The value at which the output will turn off 
 * @retval	None
 */
void PCA9685_SetOutput(uint8_t Address, uint8_t Output, uint16_t OffValue)
{
	// Optional: TWI_SlaveAtAddress(Address), might make things slower
	// if (Output <= MAX_OUTPUT_INDEX && OnValue <= MAX_OUTPUT_VALUE && OffValue <= MAX_OUTPUT_VALUE)
	// {
		TWI_BeginTransmission(Address);
		TWI_Write(LEDn_ON_L(Output));
		TWI_Write(0);			// LEDn_ON_L
		// TWI_Write(OnValue & 0xFF);			// LEDn_ON_L
		TWI_Write(0);	// LEDn_ON_H
		// TWI_Write((OnValue >> 8) & 0xF);	// LEDn_ON_H
		TWI_Write(OffValue & 0xFF);			// LEDn_OFF_L
		TWI_Write((OffValue >> 8) & 0xF);	// LEDn_OFF_H
		TWI_EndTransmission();
	// }
}

#endif /* PCA9685_H_ */

