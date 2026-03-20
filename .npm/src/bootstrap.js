import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'
import persist from '@alpinejs/persist'
import intersect from '@alpinejs/intersect'

Alpine.plugin(mask)
Alpine.plugin(persist)
Alpine.plugin(intersect)

window.Alpine = Alpine
Alpine.start()