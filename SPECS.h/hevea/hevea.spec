%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global _texmf %{_datadir}/texmf
%if !%{opt}
%global debug_package %{nil}
%endif

Name:		hevea
Version:	2.16
Release:	3%{?dist}
Summary:	LaTeX to HTML translator
Summary(zh_CN.UTF-8): LaTeX 到 HTML 的转换器
Group:		Applications/Publishing
Group(zh_CN.UTF-8): 应用程序/出版
License:	QPL
URL:		http://hevea.inria.fr/
Source0:	http://hevea.inria.fr/distri/%{name}-%{version}.tar.gz
Source1:	http://hevea.inria.fr/distri/%{name}-%{version}-manual.pdf
BuildRequires:	ocaml >= 3.12, tex(latex)
Requires:	tex(latex) netpbm-progs ghostscript tex(dvips)
Requires(post):	kpathsea
Requires(postun):	kpathsea


%description
HEVEA is a quite complete and fast LATEX to HTML translator.
HEVEA renders symbols by using the so-called HTML "entities", which
modern browsers display correctly most of the time.

%description -l zh_CN.UTF-8
LaTeX 到 HTML 的转换器。

%prep
%setup -q
cp -p %{SOURCE1} .

# Fix encoding
iconv -f iso-8859-1 -t utf-8 CHANGES > CHANGES.utf8
touch -r CHANGES CHANGES.utf8
mv -f CHANGES.utf8 CHANGES


%build
ulimit -s unlimited
make %{?_smp_mflags} \
%if ! %{opt}
	TARGET=byte \
%endif
	PREFIX=%{_prefix} \
	LIBDIR=%{_datadir}/%{name} \
	LATEXLIBDIR=%{_texmf}/tex/latex/hevea \
	OCAMLFLAGS="-g -w +a-4-9"


%install
make install \
%if ! %{opt}
	TARGET=byte \
%endif
	DESTDIR=%{buildroot}
	PREFIX=%{_prefix} \
	LIBDIR=%{_datadir}/hevea \
	LATEXLIBDIR=%{_texmf}/tex/latex/hevea
magic_rpm_clean.sh
	
%post -p /usr/bin/mktexlsr


%postun -p /usr/bin/mktexlsr


%files
%doc README CHANGES LICENSE %{name}-%{version}-manual.pdf
%{_bindir}/*
%{_datadir}/hevea
%{_texmf}/tex/latex/hevea/


%changelog
* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.16-3
- 为 Magic 3.0 重建

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 2.16-2
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Jerry James <loganjerry@gmail.com> - 2.16-1
- New upstream release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Jerry James <loganjerry@gmail.com> - 2.14-1
- New upstream release

* Wed Apr 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.13-2
- Remove ocaml_arches (see rhbz#1087794).

* Mon Mar 31 2014 Jerry James <loganjerry@gmail.com> - 2.13-1
- New upstream release
- Unbreak bytecode build

* Thu Jan 16 2014 Jerry James <loganjerry@gmail.com> - 2.12-2
- Unlimit the stack to fix the ppc64 build (really fixes bz 879050)

* Thu Jan 16 2014 Jerry James <loganjerry@gmail.com> - 2.12-1
- New upstream release
- Work around broken texlive _texmf_main macro (bz 1054317)

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 2.09-2
- Fix typo in Requires(postun)

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 2.09-1
- New upstream release (hopefully fixes bz 879050)
- Build for OCaml 4.01.0
- Enable debuginfo
- Use _texmf_main macro (bz 989703)
- Modernize the spec file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10-10
- Exclude ppc64 arches - it's not possible to build hevea on these ones

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 22 2009 Dennis Gilmore <dennis@ausil.us> - 1.10-5
- switch ExclusiveArch to ExcludeArch on arches withot ocaml

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.10-2
- Rebuild for OCaml 3.11.0+rc1.

* Mon Feb 11 2008 Andreas Thienemann <andreas@bawue.net> - 1.10-1
- Updated to 1.10

* Wed Aug 22 2007 Andreas Thienemann <andreas@bawue.net> - 1.09-3
- Added EA x86_64 as it was forgotten in -2

* Tue Aug 14 2007 Andreas Thienemann <andreas@bawue.net> - 1.09-2
- Added EA to prevent building on ppc64 until ocaml is available

* Tue Aug 14 2007 Andreas Thienemann <andreas@bawue.net> - 1.09-1
- Updated to 1.09

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 1.08-6
- FE6 Rebuild

* Mon May 01 2006 Andreas Thienemann <andreas@bawue.net> - 1.08-5
- Typofix in %%post

* Sun Apr 30 2006 Andreas Thienemann <andreas@bawue.net> - 1.08-4
- Included Requirements for imagen

* Fri Apr 28 2006 Andreas Thienemann <andreas@bawue.net> - 1.08-3
- Better comformity to FHS

* Fri Apr 28 2006 Andreas Thienemann <andreas@bawue.net> - 1.08-2
- Cleaned up and adapted for FE

* Sat Jul  2 2005 Gerard Milmeister <gemi@bluewin.ch> - 1.08-1
- New Version 1.08

* Fri Mar 19 2004 Gerard Milmeister <gemi@bluewin.ch> - 0:1.07-0.fdr.1
- First Fedora release
