
var combinationLock = {
  wheels: [0, 0, 0, 0],
  increment: function(wheel) {
    if (this.wheels[wheel] === 9) {
      this.wheels[wheel] = 0;
    } else {
      this.wheels[wheel]++;
    }
  },
  decrement: function(wheel) {
    if (this.wheels[wheel] === 0) {
      this.wheels[wheel] = 9;
    } else {
      this.wheels[wheel]--;
    }
  },
}

// Increment buttons
var increments = document.getElementsByClassName('increment');
for (var i = 0; i < increments.length; i++) {
  increments[i].addEventListener('click', function(){
    const wheelIndex = parseInt(this.getAttribute('index'));
    combinationLock.increment(wheelIndex);
    document.querySelectorAll('.digit')[wheelIndex].value = combinationLock.wheels[wheelIndex];
  });
}

// Decrement buttons
var decrements = document.getElementsByClassName('decrement');
for (var i = 0; i < decrements.length; i++) {
  decrements[i].addEventListener('click', function(){
    const wheelIndex = parseInt(this.getAttribute('index'));
    combinationLock.decrement(wheelIndex);
    document.querySelectorAll('.digit')[wheelIndex].value = combinationLock.wheels[wheelIndex];
  });
}

// Keypress
var wheels = document.getElementsByClassName('digit');
for (var i = 0; i < wheels.length; i++) {
  wheels[i].addEventListener('keyup', function(e){
    const wheelIndex = parseInt(this.getAttribute('index'));

    // arrow key up
    if (e.which === 38) {
      combinationLock.increment(wheelIndex);
      document.querySelectorAll('.digit')[wheelIndex].value = combinationLock.wheels[wheelIndex];
    }

    // arrow key down
    if (e.which === 40) {
      combinationLock.decrement(wheelIndex);
      document.querySelectorAll('.digit')[wheelIndex].value = combinationLock.wheels[wheelIndex];
    }

    // number key (0 - 9)
    if (e.which > 47 && e.which < 58 ) {
      document.querySelectorAll('.digit')[wheelIndex].value = e.key;
      combinationLock.wheels[wheelIndex] = e.key;
    }

    // if number is longer than 1 digit
    if (this.value.length > 1) {
      this.value = 0;
    }

    // if number is less that 1 digit
    if (this.value.length < 1) {
      this.value = 0;
    }
  });
}