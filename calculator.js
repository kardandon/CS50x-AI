function sum() {
    document.querySelector("#result").innerHTML = (parseFloat(document.querySelector("#number1").value) + parseFloat(document.querySelector("#number2").value)).toString()
}

function sub() {
    document.querySelector("#result").innerHTML = (parseFloat(document.querySelector("#number1").value) - parseFloat(document.querySelector("#number2").value)).toString()
}

function mul() {
    document.querySelector("#result").innerHTML = (parseFloat(document.querySelector("#number1").value) * parseFloat(document.querySelector("#number2").value)).toString()
}

function div() {
    document.querySelector("#result").innerHTML = (parseFloat(document.querySelector("#number1").value) / parseFloat(document.querySelector("#number2").value)).toString()
}