%global with_python3 1

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-lxml
Version:	3.5.0b1
Release:	3%{?dist}
Summary:        ElementTree-like Python bindings for libxml2 and libxslt
Summary(zh_CN.UTF-8): libxml2 和 libxslt 的 Python 绑定

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        BSD
URL:            http://lxml.de
Source0:        http://lxml.de/files/lxml-%{version}.tgz
Source1:        http://lxml.de/files/lxml-%{version}.tgz.asc

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxslt-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  Cython >= 0.17.1

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%description -l zh_CN.UTF-8
libxml2 和 libxslt 的 Python 绑定。

%package docs
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:      noarch
%description docs
This package provides the documentation for %{name}, e.g. the API as html.

%description docs -l zh_CN.UTF-8
%{name} 的文档。

%if 0%{?with_python3}
%package -n python3-lxml
Summary:        ElementTree-like Python 3 bindings for libxml2 and libxslt
Summary(zh_CN.UTF-8): libxml2 和 libxslt 的 Python3 绑定
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description -n python3-lxml
lxml provides a Python 3 binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python 3 Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.
%description -n python3-lxml -l zh_CN.UTF-8
libxml2 和 libxslt 的 Python3 绑定。
%endif

%prep
%setup -q -n lxml-%{version}

# remove the C extension so that it will be rebuilt using the latest Cython
rm -f src/lxml/lxml.etree.c
rm -f src/lxml/lxml.etree.h
rm -f src/lxml/lxml.etree_api.h
rm -f src/lxml/lxml.objectify.c

chmod a-x doc/rest2html.py
%{__sed} -i 's/\r//' doc/s5/ui/default/print.css \
    doc/s5/ep2008/atom.rng \
    doc/s5/ui/default/iepngfix.htc

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -r . %{py3dir}
%endif

%build
CFLAGS="%{optflags}" %{__python} setup.py build --with-cython

%if 0%{?with_python3}
cp src/lxml/lxml.etree.c %{py3dir}/src/lxml
cp src/lxml/lxml.etree.h %{py3dir}/src/lxml
cp src/lxml/lxml.etree_api.h %{py3dir}/src/lxml
cp src/lxml/lxml.objectify.c %{py3dir}/src/lxml

pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build --with-cython
popd
%endif

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --no-compile --with-cython --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --no-compile --with-cython --root %{buildroot}
popd
%endif
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt
%{python_sitearch}/lxml
%{python_sitearch}/lxml-*.egg-info

%files docs
%defattr(-,root,root,-)
%doc doc/*

%if 0%{?with_python3}
%files -n python3-lxml
%defattr(-,root,root,-)
%doc LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt
%{python3_sitearch}/lxml-*.egg-info
%{python3_sitearch}/lxml
%endif

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 3.5.0b1-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.5.0b1-2
- 更新到 3.5.0b1

* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 3.4.4-1
- 更新到 3.4.4

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 3.0.1-3
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.0.1-2
- 为 Magic 3.0 重建

* Mon Oct 15 2012 Jeffrey Ollie <jeff@ocjtech.us> - 3.0.1-1
- 3.0.1 (2012-10-14)
- Bugs fixed
-
-  * LP#1065924: Element proxies could disappear during garbage collection
-    in PyPy without proper cleanup.
-  * GH#71: Failure to work with libxml2 2.6.x.
-  * LP#1065139: static MacOS-X build failed in Py3.

* Wed Oct 10 2012 Jeffrey Ollie <jeff@ocjtech.us> - 3.0-1
- 3.0 (2012-10-08)
- ================
-
- Features added
- --------------
-
- Bugs fixed
- ----------
-
- * End-of-file handling was incorrect in iterparse() when reading from
-   a low-level C file stream and failed in libxml2 2.9.0 due to its
-   improved consistency checks.
-
- Other changes
- -------------
-
- * The build no longer uses Cython by default unless the generated C files
-   are missing.  To use Cython, pass the option "--with-cython".  To ignore
-   the fatal build error when Cython is required but not available (e.g. to
-   run special setup.py commands that do not actually run a build), pass
-   "--without-cython".
-
-
- 3.0beta1 (2012-09-26)
- =====================
-
- Features added
- --------------
-
- * Python level access to (optional) libxml2 memory debugging features
-   to simplify debugging of memory leaks etc.
-
- Bugs fixed
- ----------
-
- * Fix a memory leak in XPath by switching to Cython 0.17.1.
-
- * Some tests were adapted to work with PyPy.
-
- Other changes
- -------------
-
- * The code was adapted to work with the upcoming libxml2 2.9.0 release.
-
-
- 3.0alpha2 (2012-08-23)
- ======================
-
- Features added
- --------------
-
- * The .iter() method of elements now accepts tag arguments like "{*}name"
-   to search for elements with a given local name in any namespace.  With
-   this addition, all combinations of wildcards now work as expected:
-   "{ns}name", "{}name", "{*}name", "{ns}*", "{}*" and "{*}*".  Note that
-   "name" is equivalent to "{}name", but "*" is "{*}*".  The same change
-   applies to the .getiterator(), .itersiblings(), .iterancestors(),
-   .iterdescendants(), .iterchildren() and .itertext() methods,  the
-   strip_attributes(), strip_elements() and strip_tags() functions as well
-   as the iterparse() function.
-
- * C14N allows specifying the inclusive prefixes to be promoted to
-   top-level during exclusive serialisation.
-
- Bugs fixed
- ----------
-
- * Passing long Unicode strings into the feed() parser interface failed to
-   read the entire string.
-
- Other changes
- -------------
-
-
- 3.0alpha1 (2012-07-31)
- ======================
-
- Features added
- --------------
-
- * Initial support for building in PyPy (through cpyext).
-
- * DTD objects gained an API that allows read access to their
-   declarations.
-
- * xpathgrep.py gained support for parsing line-by-line (e.g.
-   from grep output) and for surrounding the output with a new root
-   tag.
-
- * E-factory in lxml.builder accepts subtypes of known data
-   types (such as string subtypes) when building elements around them.
-
- * Tree iteration and iterparse() with a selective tag
-   argument supports passing a set of tags.  Tree nodes will be
-   returned by the iterators if they match any of the tags.
-
- Bugs fixed
- ----------
-
- * The .find*() methods in lxml.objectify no longer use XPath
-   internally, which makes them faster in many cases (especially when
-   short circuiting after a single or couple of elements) and fixes
-   some behavioural differences compared to lxml.etree.  Note that
-   this means that they no longer support arbitrary XPath expressions
-   but only the subset that the ElementPath language supports.
-   The previous implementation was also redundant with the normal
-   XPath support, which can be used as a replacement.
-
- * el.find('*') could accidentally return a comment or processing
-   instruction that happened to be in the wrong spot.  (Same for the
-   other .find*() methods.)
-
- * The error logging is less intrusive and avoids a global setup where
-   possible.
-
- * Fixed undefined names in html5lib parser.
-
- * xpathgrep.py did not work in Python 3.
-
- * Element.attrib.update() did not accept an attrib of
-   another Element as parameter.
-
- * For subtypes of ElementBase that make the .text or .tail
-   properties immutable (as in objectify, for example), inserting text
-   when creating Elements through the E-Factory feature of the class
-   constructor would fail with an exception, stating that the text
-   cannot be modified.
-
- Other changes
- --------------
-
- * The code base was overhauled to properly use 'const' where the API
-   of libxml2 and libxslt requests it.  This also has an impact on the
-   public C-API of lxml itself, as defined in etreepublic.pxd, as
-   well as the provided declarations in the lxml/includes/ directory.
-   Code that uses these declarations may have to be adapted.  On the
-   plus side, this fixes several C compiler warnings, also for user
-   code, thus making it easier to spot real problems again.
-
- * The functionality of "lxml.cssselect" was moved into a separate PyPI
-   package called "cssselect".  To continue using it, you must install
-   that package separately.  The "lxml.cssselect" module is still
-   available and provides the same interface, provided the "cssselect"
-   package can be imported at runtime.
-
- * Element attributes passed in as an attrib dict or as keyword
-   arguments are now sorted by (namespaced) name before being created
-   to make their order predictable for serialisation and iteration.
-   Note that adding or deleting attributes afterwards does not take
-   that order into account, i.e. setting a new attribute appends it
-   after the existing ones.
-
- * Several classes that are for internal use only were removed
-   from the lxml.etree module dict:
-   _InputDocument, _ResolverRegistry, _ResolverContext, _BaseContext,
-   _ExsltRegExp, _IterparseContext, _TempStore, _ExceptionContext,
-   __ContentOnlyElement, _AttribIterator, _NamespaceRegistry,
-   _ClassNamespaceRegistry, _FunctionNamespaceRegistry,
-   _XPathFunctionNamespaceRegistry, _ParserDictionaryContext,
-   _FileReaderContext, _ParserContext, _PythonSaxParserTarget,
-   _TargetParserContext, _ReadOnlyProxy, _ReadOnlyPIProxy,
-   _ReadOnlyEntityProxy, _ReadOnlyElementProxy, _OpaqueNodeWrapper,
-   _OpaqueDocumentWrapper, _ModifyContentOnlyProxy,
-   _ModifyContentOnlyPIProxy, _ModifyContentOnlyEntityProxy,
-   _AppendOnlyElementProxy, _SaxParserContext, _FilelikeWriter,
-   _ParserSchemaValidationContext, _XPathContext,
-   _XSLTResolverContext, _XSLTContext, _XSLTQuotedStringParam
-
- * Several internal classes can no longer be inherited from:
-   _InputDocument, _ResolverRegistry, _ExsltRegExp, _ElementUnicodeResult,
-   _IterparseContext, _TempStore, _AttribIterator, _ClassNamespaceRegistry,
-   _XPathFunctionNamespaceRegistry, _ParserDictionaryContext,
-   _FileReaderContext, _PythonSaxParserTarget, _TargetParserContext,
-   _ReadOnlyPIProxy, _ReadOnlyEntityProxy, _OpaqueDocumentWrapper,
-   _ModifyContentOnlyPIProxy, _ModifyContentOnlyEntityProxy,
-   _AppendOnlyElementProxy, _FilelikeWriter, _ParserSchemaValidationContext,
-   _XPathContext, _XSLTResolverContext, _XSLTContext,
-   _XSLTQuotedStringParam, _XSLTResultTree, _XSLTProcessingInstruction

* Thu Sep 27 2012 Jeffrey Ollie <jeff@ocjtech.us> - 2.3.5-1
- Bugs fixed
-
-  * Crash when merging text nodes in element.remove().
-  * Crash in sax/target parser when reporting empty doctype.

* Thu Sep 27 2012 Jeffrey Ollie <jeff@ocjtech.us> - 2.3.4-1
- Bugs fixed
-
-  * Crash when building an nsmap (Element property) with empty namespace
-    URIs.
-  * Crash due to race condition when errors (or user messages) occur during
-    threaded XSLT processing (or compilation).
-  * XSLT stylesheet compilation could ignore compilation errors.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.3.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.3.3-3
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.3.3-1
- 2.3.3 (2012-01-04)
- Features added
-
-  * lxml.html.tostring() gained new serialisation options with_tail and
-    doctype.
-
- Bugs fixed
-
-  * Fixed a crash when using iterparse() for HTML parsing and requesting
-    start events.
-  * Fixed parsing of more selectors in cssselect. Whitespace before pseudo-
-    elements and pseudo-classes is significant as it is a descendant
-    combinator. "E :pseudo" should parse the same as "E *:pseudo", not
-    "E:pseudo". Patch by Simon Sapin.
-  * lxml.html.diff no longer raises an exception when hitting 'img' tags
-    without 'src' attribute.

* Mon Nov 14 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.3.2-1
- 2.3.2 (2011-11-11)
- Features added
-
-   * lxml.objectify.deannotate() has a new boolean option
-     cleanup_namespaces to remove the objectify namespace declarations
-     (and generally clean up the namespace declarations) after removing
-     the type annotations.
-   * lxml.objectify gained its own SubElement() function as a copy of
-     etree.SubElement to avoid an otherwise redundant import of
-     lxml.etree on the user side.
-
- Bugs fixed
-
-    * Fixed the "descendant" bug in cssselect a second time (after a first
-      fix in lxml 2.3.1). The previous change resulted in a serious
-      performance regression for the XPath based evaluation of the
-      translated expression. Note that this breaks the usage of some
-      of the generated XPath expressions as XSLT location paths that
-      previously worked in 2.3.1.
-    * Fixed parsing of some selectors in cssselect. Whitespace after
-      combinators ">", "+" and "~" is now correctly ignored. Previously
-      it was parsed as a descendant combinator. For example, "div> .foo"
-      was parsed the same as "div>* .foo" instead of "div>.foo". Patch by
-      Simon Sapin.

* Sun Sep 25 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.3.1-1
- Features added
- --------------
-
- * New option kill_tags in lxml.html.clean to remove specific
-   tags and their content (i.e. their whole subtree).
-
- * pi.get() and pi.attrib on processing instructions to parse
-   pseudo-attributes from the text content of processing instructions.
-
- * lxml.get_include() returns a list of include paths that can be
-   used to compile external C code against lxml.etree.  This is
-   specifically required for statically linked lxml builds when code
-   needs to compile against the exact same header file versions as lxml
-   itself.
-
- * Resolver.resolve_file() takes an additional option
-   close_file that configures if the file(-like) object will be
-   closed after reading or not.  By default, the file will be closed,
-   as the user is not expected to keep a reference to it.
-
- Bugs fixed
- ----------
-
- * HTML cleaning didn't remove 'data:' links.
-
- * The html5lib parser integration now uses the 'official'
-   implementation in html5lib itself, which makes it work with newer
-   releases of the library.
-
- * In lxml.sax, endElementNS() could incorrectly reject a plain
-   tag name when the corresponding start event inferred the same plain
-   tag name to be in the default namespace.
-
- * When an open file-like object is passed into parse() or
-   iterparse(), the parser will no longer close it after use.  This
-   reverts a change in lxml 2.3 where all files would be closed.  It is
-   the users responsibility to properly close the file(-like) object,
-   also in error cases.
-
- * Assertion error in lxml.html.cleaner when discarding top-level elements.
-
- * In lxml.cssselect, use the xpath 'A//B' (short for
-   'A/descendant-or-self::node()/B') instead of 'A/descendant::B' for the
-   css descendant selector ('A B'). This makes a few edge cases to be
-   consistent with the selector behavior in WebKit and Firefox, and makes
-   more css expressions valid location paths (for use in xsl:template
-   match).
-
- * In lxml.html, non-selected <option> tags no longer show up in the
-   collected form values.
-
- * Adding/removing <option> values to/from a multiple select form
-   field properly selects them and unselects them.
-
- Other changes
- --------------
-
- * Static builds can specify the download directory with the
-   --download-dir option.


* Tue Apr 19 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.3-1
- 2.3 (2011-02-06)
- ================
-
- Features added
- --------------
-
- * When looking for children, ``lxml.objectify`` takes '{}tag' as
-   meaning an empty namespace, as opposed to the parent namespace.
-
- Bugs fixed
- ----------
-
- * When finished reading from a file-like object, the parser
-   immediately calls its ``.close()`` method.
-
- * When finished parsing, ``iterparse()`` immediately closes the input
-   file.
-
- * Work-around for libxml2 bug that can leave the HTML parser in a
-   non-functional state after parsing a severly broken document (fixed
-   in libxml2 2.7.8).
-
- * ``marque`` tag in HTML cleanup code is correctly named ``marquee``.
-
- Other changes
- --------------
-
- * Some public functions in the Cython-level C-API have more explicit
-   return types.
-
- 2.3beta1 (2010-09-06)
- =====================
-
- Features added
- --------------
-
- Bugs fixed
- ----------
-
- * Crash in newer libxml2 versions when moving elements between
-   documents that had attributes on replaced XInclude nodes.
-
- * ``XMLID()`` function was missing the optional ``parser`` and
-   ``base_url`` parameters.
-
- * Searching for wildcard tags in ``iterparse()`` was broken in Py3.
-
- * ``lxml.html.open_in_browser()`` didn't work in Python 3 due to the
-   use of os.tempnam.  It now takes an optional 'encoding' parameter.
-
- Other changes
- --------------
-
- 2.3alpha2 (2010-07-24)
- ======================
-
- Features added
- --------------
-
- Bugs fixed
- ----------
-
- * Crash in XSLT when generating text-only result documents with a
-   stylesheet created in a different thread.
-
- Other changes
- --------------
-
- * ``repr()`` of Element objects shows the hex ID with leading 0x
-   (following ElementTree 1.3).
-
- 2.3alpha1 (2010-06-19)
- ======================
-
- Features added
- --------------
-
- * Keyword argument ``namespaces`` in ``lxml.cssselect.CSSSelector()``
-   to pass a prefix-to-namespace mapping for the selector.
-
- * New function ``lxml.etree.register_namespace(prefix, uri)`` that
-   globally registers a namespace prefix for a namespace that newly
-   created Elements in that namespace will use automatically.  Follows
-   ElementTree 1.3.
-
- * Support 'unicode' string name as encoding parameter in
-   ``tostring()``, following ElementTree 1.3.
-
- * Support 'c14n' serialisation method in ``ElementTree.write()`` and
-   ``tostring()``, following ElementTree 1.3.
-
- * The ElementPath expression syntax (``el.find*()``) was extended to
-   match the upcoming ElementTree 1.3 that will ship in the standard
-   library of Python 3.2/2.7.  This includes extended support for
-   predicates as well as namespace prefixes (as known from XPath).
-
- * During regular XPath evaluation, various ESXLT functions are
-   available within their namespace when using libxslt 1.1.26 or later.
-
- * Support passing a readily configured logger instance into
-   ``PyErrorLog``, instead of a logger name.
-
- * On serialisation, the new ``doctype`` parameter can be used to
-   override the DOCTYPE (internal subset) of the document.
-
- * New parameter ``output_parent`` to ``XSLTExtension.apply_templates()``
-   to append the resulting content directly to an output element.
-
- * ``XSLTExtension.process_children()`` to process the content of the
-   XSLT extension element itself.
-
- * ISO-Schematron support based on the de-facto Schematron reference
-   'skeleton implementation'.
-
- * XSLT objects now take XPath object as ``__call__`` stylesheet
-   parameters.
-
- * Enable path caching in ElementPath (``el.find*()``) to avoid parsing
-   overhead.
-
- * Setting the value of a namespaced attribute always uses a prefixed
-   namespace instead of the default namespace even if both declare the
-   same namespace URI.  This avoids serialisation problems when an
-   attribute from a default namespace is set on an element from a
-   different namespace.
-
- * XSLT extension elements: support for XSLT context nodes other than
-   elements: document root, comments, processing instructions.
-
- * Support for strings (in addition to Elements) in node-sets returned
-   by extension functions.
-
- * Forms that lack an ``action`` attribute default to the base URL of
-   the document on submit.
-
- * XPath attribute result strings have an ``attrname`` property.
-
- * Namespace URIs get validated against RFC 3986 at the API level
-   (required by the XML namespace specification).
-
- * Target parsers show their target object in the ``.target`` property
-   (compatible with ElementTree).
-
- Bugs fixed
- ----------
-
- * API is hardened against invalid proxy instances to prevent crashes
-   due to incorrectly instantiated Element instances.
-
- * Prevent crash when instantiating ``CommentBase`` and friends.
-
- * Export ElementTree compatible XML parser class as
-   ``XMLTreeBuilder``, as it is called in ET 1.2.
-
- * ObjectifiedDataElements in lxml.objectify were not hashable.  They
-   now use the hash value of the underlying Python value (string,
-   number, etc.) to which they compare equal.
-
- * Parsing broken fragments in lxml.html could fail if the fragment
-   contained an orphaned closing '</div>' tag.
-
- * Using XSLT extension elements around the root of the output document
-   crashed.
-
- * ``lxml.cssselect`` did not distinguish between ``x[attr="val"]`` and
-   ``x [attr="val"]`` (with a space).  The latter now matches the
-   attribute independent of the element.
-
- * Rewriting multiple links inside of HTML text content could end up
-   replacing unrelated content as replacements could impact the
-   reported position of subsequent matches.  Modifications are now
-   simplified by letting the ``iterlinks()`` generator in ``lxml.html``
-   return links in reversed order if they appear inside the same text
-   node.  Thus, replacements and link-internal modifications no longer
-   change the position of links reported afterwards.
-
- * The ``.value`` attribute of ``textarea`` elements in lxml.html did
-   not represent the complete raw value (including child tags etc.). It
-   now serialises the complete content on read and replaces the
-   complete content by a string on write.
-
- * Target parser didn't call ``.close()`` on the target object if
-   parsing failed.  Now it is guaranteed that ``.close()`` will be
-   called after parsing, regardless of the outcome.
-
- Other changes
- -------------
-
- * Official support for Python 3.1.2 and later.
-
- * Static MS Windows builds can now download their dependencies
-   themselves.
-
- * ``Element.attrib`` no longer uses a cyclic reference back to its
-   Element object.  It therefore no longer requires the garbage
-   collector to clean up.
-
- * Static builds include libiconv, in addition to libxml2 and libxslt.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010  David Malcolm <dmalcolm@redhat.com> - 2.2.8-3
- rebuild for newer python3

* Fri Nov  5 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.8-2
- Rebuild for newer libxml2

* Mon Sep  6 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.8-1
- 2.2.8 (2010-09-02)
- Bugs fixed
-
-     * Crash in newer libxml2 versions when moving elements between
-       documents that had attributes on replaced XInclude nodes.
-     * Import fix for urljoin in Python 3.1+.

* Tue Aug 24 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-3
- Don't byte-compile files during install because setup.py doesn't
  properly byte compile for Python version 3.2

* Sun Aug 22 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-2
- Rebuild for Python 3.2

* Mon Jul 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.7-1
- 2.2.7 (2010-07-24)
- Bugs fixed
-
-     * Crash in XSLT when generating text-only result documents with a stylesheet created in a different thread.

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-4
- actually add the patch this time

* Mon Jul 26 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-3
- workaround for 2to3 issue (patch 0; bug 600036)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Mar  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.6-1
- 2.2.6 (2010-03-02)
-
- Bugs fixed
-
-    * Fixed several Python 3 regressions by building with Cython 0.11.3.

* Mon Mar  1 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.5-1
- 2.2.5 (2010-02-28)
-
- Features added
-
-    * Support for running XSLT extension elements on the input root node
-      (e.g. in a template matching on "/").
-
- Bugs fixed
-
-    * Crash in XPath evaluation when reading smart strings from a document
-      other than the original context document.
-    * Support recent versions of html5lib by not requiring its XHTMLParser
-      in htmlparser.py anymore.
-    * Manually instantiating the custom element classes in lxml.objectify
-      could crash.
-    * Invalid XML text characters were not rejected by the API when they
-      appeared in unicode strings directly after non-ASCII characters.
-    * lxml.html.open_http_urllib() did not work in Python 3.
-    * The functions strip_tags() and strip_elements() in lxml.etree did
-      not remove all occurrences of a tag in all cases.
-    * Crash in XSLT extension elements when the XSLT context node is not
-      an element.

* Mon Feb 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.2.4-2
- update to current python3 guidelines
- be more explicit in %%files
- use %%global and not %%define
- create docs subpackage
- add stripping 3-byte Byte Order Marker from src/lxml/tests/test_errors.py
  to get 2to3 to work (dmalcolm)
- fixes FTBFS (#564674)

* Thu Jan 14 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.4-1
- Update to 2.2.4
- Enable Python 3 subpackage

* Thu Nov  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-3
- F-13's python build chain must be a little different...

* Thu Nov  5 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-2
- Add option to build a Python 3 subpackage, original patch by David Malcolm

* Fri Oct 30 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.3-1
- 2.2.3 (2009-10-30)
- Bugs fixed
-
-    * The resolve_entities option did not work in the incremental feed
-      parser.
-    * Looking up and deleting attributes without a namespace could hit a
-      namespaced attribute of the same name instead.
-    * Late errors during calls to SubElement() (e.g. attribute related
-      ones) could leave a partially initialised element in the tree.
-    * Modifying trees that contain parsed entity references could result
-      in an infinite loop.
-    * ObjectifiedElement.__setattr__ created an empty-string child element
-      when the attribute value was rejected as a non-unicode/non-ascii
-      string
-    * Syntax errors in lxml.cssselect could result in misleading error
-      messages.
-    * Invalid syntax in CSS expressions could lead to an infinite loop in
-      the parser of lxml.cssselect.
-    * CSS special character escapes were not properly handled in
-      lxml.cssselect.
-    * CSS Unicode escapes were not properly decoded in lxml.cssselect.
-    * Select options in HTML forms that had no explicit value attribute
-      were not handled correctly. The HTML standard dictates that their
-      value is defined by their text content. This is now supported by
-      lxml.html.
-    * XPath raised a TypeError when finding CDATA sections. This is now
-      fully supported.
-    * Calling help(lxml.objectify) didn't work at the prompt.
-    * The ElementMaker in lxml.objectify no longer defines the default
-      namespaces when annotation is disabled.
-    * Feed parser failed to honour the 'recover' option on parse errors.
-    * Diverting the error logging to Python's logging system was broken.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.2-1
- 2.2.2 (2009-06-21)
- Features added
-
-    * New helper functions strip_attributes(), strip_elements(),
-      strip_tags() in lxml.etree to remove attributes/subtrees/tags
-      from a subtree.
-
- Bugs fixed
-
-    * Namespace cleanup on subtree insertions could result in missing
-      namespace declarations (and potentially crashes) if the element
-      defining a namespace was deleted and the namespace was not used
-      by the top element of the inserted subtree but only in deeper
-      subtrees.
-    * Raising an exception from a parser target callback didn't always
-      terminate the parser.
-    * Only {true, false, 1, 0} are accepted as the lexical representation
-      for BoolElement ({True, False, T, F, t, f} not any more), restoring
-      lxml <= 2.0 behaviour.

* Tue Jun  2 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.1-1
- 2.2.1 (2009-06-02)
- Features added
-
-    * Injecting default attributes into a document during XML Schema
-      validation (also at parse time).
-    * Pass huge_tree parser option to disable parser security restrictions
-      imposed by libxml2 2.7.
-
- Bugs fixed
-
-    * The script for statically building libxml2 and libxslt didn't work
-      in Py3.
-    * XMLSchema() also passes invalid schema documents on to libxml2 for
-      parsing (which could lead to a crash before release 2.6.24).

* Tue Mar 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-1
- 2.2 (2009-03-21)
- Features added
-
-    * Support for standalone flag in XML declaration through
-      tree.docinfo.standalone and by passing standalone=True/False on
-      serialisation.
-
- Bugs fixed
-
-    * Crash when parsing an XML Schema with external imports from a
-      filename.

* Fri Feb 27 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.8.beta4
- 2.2beta4 (2009-02-27)
- Features added
-
-    * Support strings and instantiable Element classes as child arguments
-      to the constructor of custom Element classes.
-    * GZip compression support for serialisation to files and file-like
-      objects.
-
- Bugs fixed
-
-    * Deep-copying an ElementTree copied neither its sibling PIs and
-      comments nor its internal/external DTD subsets.
-    * Soupparser failed on broken attributes without values.
-    * Crash in XSLT when overwriting an already defined attribute using
-      xsl:attribute.
-    * Crash bug in exception handling code under Python 3. This was due to
-      a problem in Cython, not lxml itself.
-    * lxml.html.FormElement._name() failed for non top-level forms.
-    * TAG special attribute in constructor of custom Element classes was
-      evaluated incorrectly.
-
- Other changes
-
-    * Official support for Python 3.0.1.
-    * Element.findtext() now returns an empty string instead of None for
-      Elements without text content.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-0.7.beta3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.6.beta3
- 2.2beta3 (2009-02-17)
- Features added
-
-    * XSLT.strparam() class method to wrap quoted string parameters that
-     require escaping.
-
- Bugs fixed
-
-    * Memory leak in XPath evaluators.
-    * Crash when parsing indented XML in one thread and merging it with
-      other documents parsed in another thread.
-    * Setting the base attribute in lxml.objectify from a unicode string
-      failed.
-    * Fixes following changes in Python 3.0.1.
-    * Minor fixes for Python 3.
-
- Other changes
-
-    * The global error log (which is copied into the exception log) is now
-      local to a thread, which fixes some race conditions.
-    * More robust error handling on serialisation.

* Sun Jan 25 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.5.beta2
- 2.2beta2 (2009-01-25)
- Bugs fixed
-
-    * Potential memory leak on exception handling. This was due to a
-      problem in Cython, not lxml itself.
-    * iter_links (and related link-rewriting functions) in lxml.html would
-      interpret CSS like url("link") incorrectly (treating the quotation
-      marks as part of the link).
-    * Failing import on systems that have an io module.

* Fri Dec 12 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.4.beta1
- 2.2beta1 (2008-12-12)
- Features added
-
-    * Allow lxml.html.diff.htmldiff to accept Element objects,
-      not just HTML strings.
-
- Bugs fixed
-
-    * Crash when using an XPath evaluator in multiple threads.
-    * Fixed missing whitespace before Link:... in lxml.html.diff.
-
- Other changes
-
-    * Export lxml.html.parse.

* Fri Nov 28 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.3.alpha1
- Rebuild for Python 2.6

* Mon Nov 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.2.alpha1
- Don't forget to upload the sources!

* Mon Nov 24 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2-0.1.alpha1
- 2.2alpha1 (2008-11-23)
- Features added
-
-    * Support for XSLT result tree fragments in XPath/XSLT extension
-      functions.
-    * QName objects have new properties namespace and localname.
-    * New options for exclusive C14N and C14N without comments.
-    * Instantiating a custom Element classes creates a new Element.
-
- Bugs fixed
-
-    * XSLT didn't inherit the parse options of the input document.
-    * 0-bytes could slip through the API when used inside of Unicode
-      strings.
-    * With lxml.html.clean.autolink, links with balanced parenthesis, that
-      end in a parenthesis, will be linked in their entirety (typical with
-      Wikipedia links).

* Mon Nov 17 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.3-1
- 2.1.3 (2008-11-17)
- Bugs fixed
-
-    * Ref-count leaks when lxml enters a try-except statement while an
-      outside exception lives in sys.exc_*(). This was due to a problem
-      in Cython, not lxml itself.
-    * Parser Unicode decoding errors could get swallowed by other
-      exceptions.
-    * Name/import errors in some Python modules.
-    * Internal DTD subsets that did not specify a system or public ID
-      were not serialised and did not appear in the docinfo property
-      of ElementTrees.
-    * Fix a pre-Py3k warning when parsing from a gzip file in Py2.6.
-    * Test suite fixes for libxml2 2.7.
-    * Resolver.resolve_string() did not work for non-ASCII byte strings.
-    * Resolver.resolve_file() was broken.
-    * Overriding the parser encoding didn't work for many encodings.

* Fri Sep  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.2-1
- 2.1.2 (2008-09-05)
- Features added
-
-    * lxml.etree now tries to find the absolute path name of files when
-      parsing from a file-like object. This helps custom resolvers when
-      resolving relative URLs, as lixbml2 can prepend them with the path of
-      the source document.
-
- Bugs fixed
-
-    * Memory problem when passing documents between threads.
-    * Target parser did not honour the recover option and raised an exception
-      instead of calling .close() on the target.

* Fri Jul 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.1-1
- Update to 2.1.1

* Fri Jun 20 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.7-1
- Update to 2.0.7
- Update download URL

* Sat May 31 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.6-1
- Update to 2.0.6

* Thu May  8 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.5-1
- Update to 2.0.5

* Wed Mar 26 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.3-1
- Update to 2.0.3

* Sat Feb 23 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.2-1
- Update to 2.0.2

* Tue Feb 19 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.0.1-1
- Update to 2.0.1

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.6-2
- Autorebuild for GCC 4.3

* Mon Nov  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.6-1
- Update to 1.3.6.

* Mon Oct 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.5-1
- Update to 1.3.5.

* Thu Aug 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.4-1
- Update to 1.3.4.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.3.3-3
- Rebuild for selinux ppc32 issue.

* Tue Aug 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-2
- BR python-setuptools-devel

* Mon Jul 30 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.3.3-1
- Update to 1.3.3

* Fri Jan 19 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.1.2-1
- Update to 1.1.2

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.0.3-3
- Rebuild for new Python

* Sat Sep 16 2006 Shahms E. King <shahms@shahms.com> 1.0.3-2
- Rebuild for FC6

* Thu Aug 17 2006 Shahms E. King <shahms@shahms.com> 1.0.3-1
- Update to new upstream version

* Fri Aug 11 2006 Shahms E. King <shahms@shahms.com> 1.0.2-2
- Include, don't ghost .pyo files per new guidelines

* Fri Jul 07 2006 Shahms E. King <shahms@shahms.com> 1.0.2-1
- Update to new upstream release

* Mon Jun 26 2006 Shahms E. King <shahms@shahms.com> 1.0.1-1
- Update to new upstream release

* Fri Jun 02 2006 Shahms E. King <shahms@shahms.com> 1.0-1
- Update to new upstream 1.0 release

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-3
- Add python-setuptools to BuildRequires
- Use dist tag

* Wed Apr 26 2006 Shahms E. King <shahms@shahms.com> 0.9.1-2
- Fix summary and description

* Tue Apr 18 2006 Shahms E. King <shahms@shahms.com> 0.9.1-1
- update the new upstream version
- remove Pyrex build req

* Tue Dec 13 2005 Shahms E. King <shahms@shahms.com> 0.8-1
- Initial package
