async function renderPage() {
  const dish = await loadDish()

  if (!dish) {
    return console.error("No dish received")
  }

  renderName()
  renderImage()
  renderIngredients()
  renderEnergy()
  renderDescription()
  renderInstructions()

  function renderName() {
    document.querySelector("h1").innerHTML = dish.name
  }

  function renderImage() {
    document.querySelector('.top__photo').innerHTML = `<img src="${dish.image}" alt="">`
  }

  function renderIngredients() {
    let htmlCode = ""
    try {
      dish.ingredient.forEach(ingredient => {
        htmlCode += getIngredientHTML(ingredient)
      })
    } catch (e) {
      console.error("Wrong ingredients format")
    } finally {
      document.querySelector(".ingredients__list").innerHTML = htmlCode
    }
  }

  function getIngredientHTML(ingredient) {
    return `<li class="ingredients__element">
              <p class="ingredients__name">${ingredient.name}</p>
              <div class="ingredients__line"></div>
              <p class="ingredients__quantity">${ingredient.quantity}</p>
              <p class="ingredients__units">${ingredient.unit}</p>
            </li>`
  }

  function renderEnergy() {
    const energyQuantityElements = document.querySelectorAll(".energy__quantity")
    energyQuantityElements[0].innerHTML = dish.calories
    energyQuantityElements[1].innerHTML = dish.proteins
    energyQuantityElements[2].innerHTML = dish.fats
    energyQuantityElements[3].innerHTML = dish.carbohydrates
  }

  function renderDescription() {
    if (!dish.description) {
      return
    }

    document.querySelector(".description").innerHTML = dish.description
  }

  function renderInstructions() {
    let htmlCode = ""
    try {
      dish.instruction.forEach(instruction => {
        htmlCode += getInstructionHTML(instruction)
      })
    } catch (e) {
      console.error("Wrong instructions format")
    } finally {
      document.querySelector(".instruction__steps").innerHTML = htmlCode
    }
  }

  function getInstructionHTML(instruction) {
    return `<li class="instruction__step">
            <p class="instruction__step-number">${instruction.number}</p>
            <p class="instruction__step-content">${instruction.text}</p>
          </li>`
  }
}

async function loadDish() {
  const urlParts = location.href.split("/").filter(Boolean)
  const dishSlag = urlParts.pop()
  return await Request.getDishInfo(dishSlag)
}

addEventListener("load", renderPage);