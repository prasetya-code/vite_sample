document.addEventListener('alpine:init', () => {

  Alpine.data('dropdown', () => ({
    open: false,
    toggle() { this.open = !this.open },
  }))

  Alpine.data('modal', () => ({
    show: false,
    open()  { this.show = true },
    close() { this.show = false },
  }))

})