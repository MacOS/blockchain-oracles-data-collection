autocmd FileType python set tabstop=8|set softtabstop=4|set shiftwidth=4| set expandtab

set colorcolumn=110
highlight ColorColumn ctermbg=darkgray

augroup project
	autocmd!
	autocmd BufRead,BufNewFile *.h,*.c set filetype =c.doxygen
augroup end
