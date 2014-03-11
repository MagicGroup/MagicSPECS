;;; site-start.el - loaded at startup before "~/.xemacs/init.el"
;;;
;;; The "-no-site-file" option to xemacs prevents this file from being loaded.

;;; psgml catalog list
(setq sgml-catalog-files
	      (if (getenv "SGML_CATALOG_FILES")
		  (split-path (getenv "SGML_CATALOG_FILES"))
		(list "CATALOG" "catalog"
		      "/etc/sgml/catalog"
		      "/etc/xml/catalog"
		      (locate-data-file "CATALOG"))))

;; default to non-kerberos ftp
(setq efs-ftp-program-name "/usr/bin/ftp")

;; default to unified diffs
(setq-default diff-switches "-u")

;; decrease lazy-lock default threshold
(setq-default lazy-lock-minimum-size (* 2 1024))

;; load .el files in "site-start.d/"
(let ((files (directory-files
              "/usr/share/xemacs/site-packages/lisp/site-start.d" t "\\.el$")))
  (mapc 'load-file files))

;; fix default courier italics
;; for courier, oblique usually produces better results than italic
(setq try-oblique-before-italic-fonts t)
(when window-system
  (make-face-italic 'italic)
  (make-face-italic 'bold-italic))

;; Set up language environment and coding systems
(when (featurep 'mule)
  (let* ((locale (getenv "LANG"))
         (lang-region (and locale
                           (substring locale 0 (min 5 (length locale)))))
         (lang (and lang-region
                    (substring lang-region 0 (min 2 (length lang-region))))))
    (cond ((equal lang "af")
           (set-language-environment "Afrikaans"))
          ((equal lang "sq")
           (set-language-environment "Albanian"))
          ((equal lang "ca")
           (set-language-environment "Catalan"))
          ((or (equal lang-region "zh_TW") (equal lang-region "zh_HK"))
           (set-language-environment "Chinese-BIG5"))
          ((or (equal lang-region "zh_CN") (equal lang-region "zh_SG"))
           (set-language-environment "Chinese-GB"))
          ((equal lang "hr")
           (set-language-environment "Croatian"))
          ((equal lang "ru")
           (set-language-environment "Cyrillic-KOI8"))
          ((equal lang "cs")
           (set-language-environment "Czech"))
          ((equal lang "da")
           (set-language-environment "Danish"))
          ((equal lang "nl")
           (set-language-environment "Dutch"))
          ((equal lang "et")
           (set-language-environment "Estonian"))
          ((equal lang "fi")
           (set-language-environment "Finnish"))
          ((equal lang "fr")
           (set-language-environment "French"))
          ((equal lang "gl")
           (set-language-environment "Galician"))
          ((equal lang "de")
           (set-language-environment "German"))
          ((equal lang "el")
           (set-language-environment "Greek"))
          ((equal lang "kl")
           (set-language-environment "Greenlandic"))
          ((or (equal lang "he") (equal lang "iw"))
           (set-language-environment "Hebrew"))
          ((equal lang "hu")
           (set-language-environment "Hungarian"))
          ((equal lang "ga")
           (set-language-environment "Irish"))
          ((equal lang "it")
           (set-language-environment "Italian"))
          ((equal lang "ja")
           (set-language-environment "Japanese"))
          ((equal lang "ko")
           (set-language-environment "Korean"))
          ((equal lang "lt")
           (set-language-environment "Lithuanian"))
          ((equal lang "mt")
           (set-language-environment "Maltese"))
          ((or (equal lang "nb") (equal lang "nn") (equal lang "no"))
           (set-language-environment "Norwegian"))
          ((equal lang "pl")
           (set-language-environment "Polish"))
          ((equal lang "pt")
           (set-language-environment "Portuguese"))
          ((equal lang "ro")
           (set-language-environment "Romanian"))
          ((equal lang "sk")
           (set-language-environment "Slovak"))
          ((equal lang "sl")
           (set-language-environment "Slovenian"))
          ((equal lang "es")
           (set-language-environment "Spanish"))
          ((equal lang "sv")
           (set-language-environment "Swedish"))
          ((equal lang "th")
           (set-language-environment "Thai-XTIS"))
          ((equal lang "tr")
           (set-language-environment "Turkish"))
          ((equal lang "vi")
           (set-language-environment "Vietnamese"))
          (t
           (set-language-environment "English")))

    ;; set-language-environment changes the locale; restore it.
    (setenv "LANG" locale)
    (set-current-locale (or locale "C"))

    (let* ((tmp (shell-command-to-string "locale charmap"))
           (tmp (substring tmp 0 (string-match "\[ \t\n\]" tmp)))
           (tmp (intern (downcase tmp))))
      (when (find-coding-system tmp)
        (let ((cat (or (coding-system-category tmp) tmp)))
            (set-coding-priority-list (list cat))
            (set-coding-category-system cat tmp))
        (set-default-output-coding-systems tmp)
        (set-keyboard-coding-system tmp)
        (set-terminal-coding-system tmp)
        (setq file-name-coding-system tmp)
        (setq process-coding-system-alist (cons (cons ".*" tmp) '()))
        (define-coding-system-alias 'native tmp)))

    ;; Register available Input Methods.
    (load "leim-list" t)
    (when (member lang '("ja" "ko" "zh"))
      ;; ispell doesn't support CJK
      (setq-default ispell-local-dictionary "english"))))

;; Set input mode
;(let ((value (current-input-mode)))
;  (set-input-mode (nth 0 value)
;                  (nth 1 value)
;                  (terminal-coding-system)
;                  ;; This quit value is optional
;                  (nth 3 value)))

;; try to preserve user/group when saving files
(setq-default backup-by-copying-when-mismatch t)

;; when saving a buffer always end it with a newline
(setq-default require-final-newline t)

;; the graphical progress bar is buggy - disable it by default (#188973)
(setq-default progress-feedback-use-echo-area t)
