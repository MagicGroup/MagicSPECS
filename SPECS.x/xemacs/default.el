;;; default.el - loaded at startup after "~/.xemacs/init.el" by default
;;;
;;; Setting `inhibit-default-init' to non-nil in "~/.xemacs/init.el"
;;; prevents loading of this file.  The "-q" option to xemacs
;;; prevents "~/.xemacs/init.el" *and* this file from being loaded
;;; at startup.

;; enable wheel mouse support by default
(when window-system
  (mwheel-install))

;; make gnus save articles be mbox format not rmail format
(defvar gnus-default-article-saver 'gnus-summary-save-in-file)

;; use terminfo by default
(defvar system-uses-terminfo t)

;; turn on syntax highlighting by default if lazy-lock is available
(when (fboundp 'turn-on-lazy-lock)
  (require 'font-lock)
  ;; use lazy-lock by default if lazy-shot is not enabled
  (remove-hook 'font-lock-mode-hook 'turn-on-lazy-lock)
  (add-hook 'font-lock-mode-hook
            (function
             (lambda ()
               (unless (and (boundp 'lazy-shot-mode) lazy-shot-mode)
                 (turn-on-lazy-lock))))
            t))
