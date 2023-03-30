addEventListener('load', async () => {
  await Filters.renderEquipment()
  await Ingredients.loadIngredients()
  Filters.renderIngredientsGroups()
  document.querySelector('.ingredients__back').addEventListener('click', e => {
    e.preventDefault()
    Filters.toggleIngredientsGroup()
  })
})