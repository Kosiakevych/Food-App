class Request {
  static async loadMoreDishes(currentDishNumber) {
    const url = `/api/v1/?offset=${currentDishNumber}`
    return await this.sendRequest(url)
  }

  static async getDishInfo(dishSlag) {
    const url = '/api/v1/dish/' + dishSlag
    return await this.sendRequest(url)
  }

  static async loadIngredients() {
    const url = '/api/v1/ingredient-filter/'
    return await this.sendRequest(url)
  }

  static async loadEquipment() {
    const url = 'api/v1/equipment-filter'
    return await this.sendRequest(url)
  }

  static async sendRequest(url, type = 'GET', body) {
    const response = await fetch(url)
    return await response.json()
  }
}
