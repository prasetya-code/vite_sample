document.addEventListener('alpine:init', () => {

  // ✅ $persist dipanggil via init() bukan saat definisi objek
  Alpine.data('counter', () => ({
    count: 0,
    init() {
      this.count = this.$persist(0).as('counter_value')
    }
  }))

  // ✅ open: false — tertutup saat pertama load
  Alpine.data('dropdown', () => ({
    open: false,
    toggle() { this.open = !this.open },
    close() { this.open = false }
  }))

  Alpine.data('modal', () => ({
    show: false,
    open()  { this.show = true },
    close() { this.show = false },
  }))

})