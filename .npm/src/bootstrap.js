import Alpine from 'alpinejs'
import mask from '@alpinejs/mask'
import persist from '@alpinejs/persist'
import intersect from '@alpinejs/intersect'
import collapse from '@alpinejs/collapse'
import focus from '@alpinejs/focus'

Alpine.plugin(mask)
Alpine.plugin(persist)
Alpine.plugin(intersect)
Alpine.plugin(collapse)
Alpine.plugin(focus)

window.Alpine = Alpine
Alpine.start()