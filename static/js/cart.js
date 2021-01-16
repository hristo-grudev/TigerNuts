var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.lenght; i++) {
    updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.Log('productID:', productId, 'Action:', action)

    })
}