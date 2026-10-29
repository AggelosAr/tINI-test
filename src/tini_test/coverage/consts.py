
STORE             = 'CoverageReport'
METADATA_FILE     = '.coverage'
STYLE_FILE        = 'style.css'
SVG_FILE          = '.coverage.svg'


_TOGGLE_SCRIPT = '''
    document.querySelectorAll('.cov-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
        if (b.dataset.status === 'comment') {
            var on = document.querySelector('.code-block').classList.toggle('show-' + 'inline-comment');
        }
        var on = document.querySelector('.code-block').classList.toggle('show-' + b.dataset.status);
        b.classList.toggle('active', on);
    });
});
'''