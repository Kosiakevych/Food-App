class Filters {
  static openedIngredientsGroupName = ''

  static renderIngredientsGroups() {
    Ingredients.getGroupNames().forEach(groupName => {
      const dishesNumber = Ingredients.ingredients[groupName].length
      const button = document.createElement('button')
      button.className = 'ingredients__group'
      button.innerHTML =
        `<span class="ingredients__group-name">${groupName}</span>
         <span class="ingredients__group-dishes">(${dishesNumber})</span>`
      button.addEventListener('click', () => {
        this.toggleIngredientsGroup()
        this.openIngredientsGroup(groupName)
      })
      document.querySelector('.ingredients__groups').appendChild(button)
    })

    const height = document.querySelector('.ingredients__groups').offsetHeight
    document.querySelector('.ingredients').style.height = height + 'px'
  }

  static openIngredientsGroup(groupName) {
    if (this.openedIngredientsGroupName === groupName) {
      return
    }

    this.openedIngredientsGroupName = groupName
    let ingredientsHTML = ''
    const ingredients = Ingredients.ingredients[groupName]
    ingredients.forEach(ingredient => {
      const name = ingredient.name
      ingredientsHTML +=
        `<input type="checkbox" id="${name}">
         <label for="${name}">${name}</label>`
    })
    const listElement = document.querySelector('.ingredients__list')
    listElement.scrollTo(0, 0)
    listElement.innerHTML = ingredientsHTML
  }

  static toggleIngredientsGroup() {
    const selector = '.ingredients__groups'
    const classList = 'ingredients__groups-closed'
    document.querySelector(selector).classList.toggle(classList)
  }

  static async renderEquipment() {
    const equipment = await Request.loadEquipment()
    console.log(equipment)

    let equipmentHTML = ''
    equipment.forEach(item => {
      const name = item.name
      equipmentHTML +=
        `<input type="checkbox" id="${name}">
         <label for="${name}">${name}</label>`
    })
    const listElement = document.querySelector('.equipment-list')
    listElement.innerHTML = equipmentHTML
  }
}