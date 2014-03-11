;; anthy-init.el
;;
(if (featurep 'xemacs)
    (setq load-path (cons "/usr/share/xemacs/xemacs-packages/lisp/anthy" load-path))
  (setq load-path (cons "/usr/share/emacs/site-lisp/anthy" load-path)))
(autoload 'anthy-leim-activate "anthy" nil t)
(register-input-method "japanese-anthy" "Japanese"
		       'anthy-leim-activate "[anthy]"
		       "Anthy Kana Kanji conversion system")

