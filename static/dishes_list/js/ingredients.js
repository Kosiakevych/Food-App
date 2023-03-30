class Ingredients {
  static ingredients = {}

  static async loadIngredients() {
    const ingredients = await Request.loadIngredients()
    this.setIngredients(ingredients)
  }

  static setIngredients(ingredients) {
    this.ingredients = {}
    ingredients.forEach(ingredient => {
      const letters = this.getIngredientFirstLetters(ingredient)
      letters.forEach(letter => {
        if (!this.ingredients[letter]) {
          this.ingredients[letter] = []
        }
        this.ingredients[letter].push(ingredient)
      })
    })
  }

  static getIngredientFirstLetters(ingredient) {
    const firstLetters = []

    ingredient.name.split(' ').forEach(word => {
      word = word.replace( /[^\p{Letter}]/gu , '')

      if (word.length) {
        firstLetters.push(word[0].toUpperCase())
      }
    })

    return firstLetters
  }

  static getGroupNames() {
    const letters = []
    for (let group in this.ingredients) {
      if (group.length === 1) {
        letters.push(group)
      }
    }
    letters.sort(this.compareLetters)

    return [...letters]
  }

  static compareLetters(a, b) {
    const cyrillicPattern = /[А-яёії]/gu
    const latinPattern = /[a-zA-Z]/gu

    if (cyrillicPattern.test(a) && latinPattern.test(b)) {
      return -1
    }

    if (latinPattern.test(a) && cyrillicPattern.test(b)) {
      return 1
    }

    if (a > b) return 1
    if (a < b) return -1
    return 0
  }
}