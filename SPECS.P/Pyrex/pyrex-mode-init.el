;; Load the pyrex-mode for .pyx files.

(autoload 'pyrex-mode "pyrex-mode" "Major mode for editing Pyrex code." t)
(add-to-list 'auto-mode-alist '("\\.pyx\\'" . pyrex-mode))




