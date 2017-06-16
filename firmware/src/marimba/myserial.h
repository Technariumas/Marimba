class MySerial{
  protected:
    volatile rx_buffer_index_t _rx_buffer_head;
    volatile rx_buffer_index_t _rx_buffer_tail;
    unsigned char _rx_buffer[SERIAL_RX_BUFFER_SIZE];

  public:
  	void begin(uint16_t baudrate) {
	    #define BAUD 115200
	    #include <util/setbaud.h>
	    UBRR0H = UBRRH_VALUE;
	    UBRR0L = UBRRL_VALUE;
    	UCSR0A |= _BV(U2X0);
    	UCSR0B = _BV(RXCIE0) | _BV(RXEN0);
	    UCSR0C = _BV(UCSZ00) | _BV(UCSZ01);
  	}

    uint8_t available() {
		return ((unsigned int)(SERIAL_RX_BUFFER_SIZE + _rx_buffer_head - _rx_buffer_tail)) % SERIAL_RX_BUFFER_SIZE;
    }

    uint8_t read() {
		// if the head isn't ahead of the tail, we don't have any characters
		if (_rx_buffer_head == _rx_buffer_tail) {
			return -1;
		} else {
			unsigned char c = _rx_buffer[_rx_buffer_tail];
			_rx_buffer_tail = (rx_buffer_index_t)(_rx_buffer_tail + 1) % SERIAL_RX_BUFFER_SIZE;
			return c;
		}
    }

    void write(uint8_t t) {  
    }

	void _rx_complete_irq(void) {
	  if (bit_is_clear(UCSR0A, UPE0)) {
	    // No Parity error, read byte and store it in the buffer if there is
	    // room
	    unsigned char c = UDR0;
	    rx_buffer_index_t i = (unsigned int)(_rx_buffer_head + 1) % SERIAL_RX_BUFFER_SIZE;

	    // if we should be storing the received character into the location
	    // just before the tail (meaning that the head would advance to the
	    // current location of the tail), we're about to overflow the buffer
	    // and so we don't write the character or advance the head.
	    if (i != _rx_buffer_tail) {
	      _rx_buffer[_rx_buffer_head] = c;
	      _rx_buffer_head = i;
	    } else {
	    	healthStatus |= HEALTH_NO_HAMMER;
	    }
	  } else {
	    // Parity error, read byte but discard it
	    UDR0;
	  };
	}

};

MySerial mySerial;

ISR(USART_RX_vect,ISR_BLOCK){
	mySerial._rx_complete_irq();
}
