"use strict";

(function() {
    document.addEventListener("DOMContentLoaded", function() {
        const pageSizeSelect = document.getElementById('page-size');

        function updateURL(page, size) {
            const currentURL = new URL(window.location.href);
            currentURL.searchParams.set('page', page);
            currentURL.searchParams.set('size', size);
            window.location.href = currentURL.toString();
        }

        function handlePageSizeChange() {
            const newPageSize = pageSizeSelect.value;

            updateURL(1, newPageSize);
        }

        pageSizeSelect.addEventListener('change', handlePageSizeChange);
    });
})();