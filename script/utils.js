
$( document ).ready(() => {
    $('input.showAll').on('click', (ev) => {
        $('.word, .hanja, .meaning, .word>span').removeClass('hidden')
    })
    $('input.hideTranslation').on('click', (ev) => {
        $('.meaning').addClass('hidden')
        $('.word, .hanja, .word>span').removeClass('hidden')
    })
    $('input.hideWord').on('click', (ev) => {
        $('.meaning').removeClass('hidden')
        $('.word, .hanja, .word>span').addClass('hidden')
    })
});
