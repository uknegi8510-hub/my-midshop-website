
// this is for qty increase or decrease
function increase(btn){

    let cartItem = btn.closest(".cart-item")

    let qty = cartItem.querySelector(".qty")
    let price = cartItem.querySelector(".price").dataset.price
    let subtotal = cartItem.querySelector(".subtotal")

    let count = parseInt(qty.innerText)

    count++
    qty.innerText = count

    subtotal.innerText = "₹" + (count * price)

    updateTotal()
}

function decrease(btn){

    let cartItem = btn.closest(".cart-item")

    let qty = cartItem.querySelector(".qty")
    let price = cartItem.querySelector(".price").dataset.price
    let subtotal = cartItem.querySelector(".subtotal")

    let count = parseInt(qty.innerText)

    if(count > 1){
        count--
        qty.innerText = count
    }

    subtotal.innerText = "₹" + (count * price)

    updateTotal()
}

function updateTotal(){

    let subtotals = document.querySelectorAll(".subtotal")
    let total = 0

    subtotals.forEach(item=>{
        total += parseFloat(item.innerText.replace("₹",""))
    })

    document.getElementById("cart-total").innerText = "₹" + total
}

function updateTotal(){

    let subtotals = document.querySelectorAll(".subtotal")
    let subtotal = 0

    subtotals.forEach(item=>{
        subtotal += parseFloat(item.innerText.replace("₹",""))
    })

    document.getElementById("subtotal").innerText = "₹" + subtotal

    // discount logic
    let discountPercent = 10
    let discountAmount = (subtotal * discountPercent) / 100

    document.getElementById("discount").innerText = "₹" + discountAmount

    // shipping
    let shipping = 50

    document.getElementById("shipping").innerText = "₹" + shipping

    // final total
    let total = subtotal - discountAmount + shipping

    document.getElementById("cart-total").innerText = "₹" + total
}


let currentStep = 1;

function nextStep(){

    if(currentStep == 1){
        document.getElementById("step1").classList.add("completed");
        document.getElementById("line1").classList.add("active");
        document.getElementById("step2").classList.add("active");
    }

    if(currentStep == 2){
        document.getElementById("step2").classList.add("completed");
        document.getElementById("line2").classList.add("active");
        document.getElementById("step3").classList.add("active");
    }

    if(currentStep == 3){
        document.getElementById("step3").classList.add("completed");
    }
   

    currentStep++;
}