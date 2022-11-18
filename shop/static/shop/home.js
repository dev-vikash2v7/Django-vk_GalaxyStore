  // find out the cart from local storage

  if (localStorage.getItem('cart') == null) {
    var cart = {};
}
else {
    cart = JSON.parse(localStorage.getItem('cart'))
    updateCart(cart)

}



// if cart button clicked then item increement done
$('.divpr').on('click', 'button.cart', function () {
    var idStr = this.id;

    // 'idstr = ',pr6(in str) ,
    // 'this =',<button class="btn btn-success cart" id="pr{{ i.id }}">Add To Cart</button> ,

    if (cart[idStr] != undefined) {
        qty = cart[idStr][0] + 1;
    }
    else {
        qty = 1;
        name_ = document.getElementById(`name${idStr}`).innerText
        price = parseInt(document.getElementById(`price${idStr}`).innerText)
        cart[idStr] = [qty, name_, price];
    }

    updateCart(cart)
});

// pop over

$('#popcart').popover();
updateCart(cart)

function updatePopover(cart) {
    console.log('inside pop cart')
    let popStr = "";
    popStr += '<h6>cart for your items in shopping cart :</h6> <div class="mx-2 my-2">';
    var i = 1

    for (var item in cart) {
        popStr += `<br> ${i} </b>)`;
        popStr += document.getElementById(`name${item}`).innerHTML.slice(0, 5) + `...Qty : <b>${cart[item][0]}</b> , <b>${cart[item][2]} Rs</b>`
        i += 1;

    }
    popStr += `</div>
     <a href="/checkout" class="btn btn-primary" id="checkout">CheckOut</a>
      <a class="btn btn-primary" id="clearCart" onclick="clearCart()">Clear Cart</a>`;

    // document.getElementById('popcart').setAttribute('data-content', popStr)
    $('#popcart').popover('show')

}

// clear the cart -button
function clearCart() {
    cart = JSON.parse(localStorage.getItem('cart'));
    for (var item in cart) {
        document.getElementById(`div${item}`).innerHTML = `<button class="btn btn-success cart" id=${item}>Add To Cart</button>`
    }
    localStorage.clear();
    cart = {};
    updateCart(cart);
}


//update cart
function updateCart(cart) {
    var sum = 0;

    for (var item in cart) {
        sum += cart[item][0]
        document.getElementById(`div${item}`).innerHTML = `
        <button id="minus${item}" class = 'btn btn-primary minus'> - </button> 
        <span id="val${item}"> ${cart[item][0]} </span>
         <button id="plus${item}" class="plus btn btn-primary"> + </button>`
    }

    localStorage.setItem('cart', JSON.stringify(cart));
    // document.getElementById('cart_no').innerText = sum;
    updatePopover(cart)

};



// change the plus minus value
$('.divpr').on('click', 'button.minus', function () {

    a = this.id.slice(7,);
    cart['pr' + a][0] -= 1;
    cart['pr' + a][0] = Math.max(0, cart['pr' + a][0])

    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0]

    if (cart['pr' + a][0] == 0) {
        document.getElementById('divpr' + a).innerHTML = `<button id=pr${a} class='btn btn-primary cart'> Add to Cart </button>`
        delete cart['pr' + a]
    }
    else {
        document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0];
    }
    updateCart(cart)
}
);

$('.divpr').on('click', 'button.plus', function () {
    a = this.id.slice(6,)
    cart['pr' + a][0] += 1;
    document.getElementById('valpr' + a).innerHTML = cart['pr' + a][0]
    updateCart(cart)
})
