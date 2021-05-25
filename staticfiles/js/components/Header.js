class Header {
    constructor(counter) {
        this.counter = counter;
        this.api = api;
        this.counterId = this.counterId.textContent;
        this.plusCounter = this.plusCounter.bind(this);
        this.minusCounter = this.minusCounter.bind(this);
    }

    plusCounter  ()  {
        this.counterId = ++this.counterId;
        this.counterId.text = this.counterId;
    }
    minusCounter ()  {
        this.counterId = --this.counterId;
        this.counterId.text = this.counterId;
    }
}
