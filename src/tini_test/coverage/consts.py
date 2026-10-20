
STORE             = 'CoverageReport'
METADATA_FILE     = '.coverage'
STYLE_FILE        = 'style.css'


_TOGGLE_SCRIPT = '''
    document.querySelectorAll('.cov-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
        var on = document.querySelector('.code-block').classList.toggle('show-' + b.dataset.status);
        b.classList.toggle('active', on);
    });
});
'''