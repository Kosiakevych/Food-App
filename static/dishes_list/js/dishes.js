let dishesNumber = 0
const dishesListElement = document.querySelector('.dishes__list')
const observerElement = document.querySelector('.dishes__observer')

new IntersectionObserver(async payload => {
  if (payload[0].isIntersecting) {
    await loadMoreDishes()
  }
}).observe(observerElement)

async function loadMoreDishes() {
  const dishes = await Request.loadMoreDishes(dishesNumber)
  dishesNumber += dishes.length
  let newDishesHtmlCode = ''
  dishes.forEach(dish => newDishesHtmlCode += generateDishHtmlCode(dish))
  dishesListElement.innerHTML += newDishesHtmlCode

  function generateDishHtmlCode(dish) {
    console.log(dish)
    const bookmarkChecked = dish.is_favourite ? "checked" : ""
    return `<div class="dishes__dish dish">
              <div class="dish__image-wrapper">
                <div class="dish__image"
                    style="background-image: url('${dish.image}')">
                </div>
              </div>
              <div class="dish__text">
                <a class="dish__name" href="dish/${dish.url}">${dish.name}</a>
                <a class="dish__category" href="#">
                  ${dish.category}
                </a>
                <a class="dish__cuisine" href="#">
                  ${dish.cuisine}
                </a>
              </div>
              <div class="dish__stars">
                <div class="dish__star"></div>
                <div class="dish__star"></div>
                <div class="dish__star"></div>
                <div class="dish__star"></div>
                <div class="dish__star"></div>
              </div>
              <div class="dish__parameters">
                <div class="parameter">
                  <div class="parameter__icon parameter__icon-ingredients"></div>
                  <div class="parameter__value">${dish.ingredient_count}</div>
                </div>
                <div class="parameter">
                  <div class="parameter__icon parameter__icon-portions"></div>
                  <div class="parameter__value">${dish.portions}</div>
                </div>
                <div class="parameter">
                  <div class="parameter__icon parameter__icon-time"></div>
                  <div class="parameter__value">${dish.time}</div>
                </div>
              </div>
              <div class="dish__bookmark">
                <input type="checkbox" id="${dish.name}"
                        class="dish-img-button"
                        "${bookmarkChecked}">
                <label for="${dish.name}">
                  <svg class="dish-img-icon">
                    <use href="../../static/img/icons.svg#icon-bookmark"></use>
                  </svg>
                </label>
              </div>
            </div>`
  }
}