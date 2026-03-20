document.addEventListener('alpine:init', () => {

  Alpine.data('counter', () => ({
    // $persist menyimpan nilai ke localStorage dengan key 'counter_value'
    // Nilai awal 0, tapi jika sudah pernah diubah akan pakai nilai tersimpan
    count: Alpine.$persist(0).as('counter_value'),

    // Tambah nilai count sebesar 1
    increment() { this.count++ },

    // Kurangi nilai count sebesar 1
    decrement() { this.count-- },

    // Reset count ke 0 dan hapus dari localStorage
    reset()     { this.count = 0 }
  }))


  Alpine.data('dropdown', () => ({
    // Dropdown tertutup saat pertama kali dimuat
    open: false,

    // Balik status: jika buka → tutup, jika tutup → buka
    toggle() { this.open = !this.open },

    // Paksa tutup dropdown (dipakai saat klik item atau klik luar)
    close()  { this.open = false }
  }))


  Alpine.data('modal', () => ({
    // Modal tersembunyi saat pertama kali dimuat
    show: false,

    // Tampilkan modal
    open()  { this.show = true },

    // Sembunyikan modal
    close() { this.show = false }
  }))

})