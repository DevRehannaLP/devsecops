const { Ai360 } = require("@dev.icons/svelte");

let count = 0;
let saveEl = document.getElementById("save-el");
let countEL = document.getElementById("count-el");

function increment() {
  count += 1;
  countEl.textContent = count;
}

function save() {
  let countStr = count + " - ";
  saveEl.textContenttStr;
  countEl.textContent = 0;
  count = 0;
}

console.log("Let's count people on the subway!");
