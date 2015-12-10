# The patchlevel does not appear in the download URL
%global majver 1.8

Name:		E
Version:	1.8.001
Release:	3%{?dist}
Summary:	Equational Theorem Prover
Group:		Applications/Engineering
License:	GPLv2+ or LGPLv2+
URL:		http://www.eprover.org/
Source0:	http://www4.in.tum.de/~schulz/WORK/E_DOWNLOAD/V_%{majver}/%{name}.tgz

# Building actually checks for specific versions of python; building may
# need to be updated for new versions of python 2:
BuildRequires:	python
BuildRequires:	help2man
BuildRequires:	tex(latex)
BuildRequires:	tex(supertabular.sty)
# You can verify the CASC results here: http://www.cs.miami.edu/~tptp/CASC/J4/

%description
E is a purely equational theorem prover for full first-order logic.
That means it is a program that you can stuff a mathematical
specification (in first-order format) and a hypothesis into, and which
will then run forever, using up all of your machines' resources.  Very
occasionally it will find a proof for the hypothesis and tell you so.

E's inference core is based on a modified version of the superposition
calculus for equational clausal logic.  Both clausification and
reasoning on the clausal form can be documented in checkable proof
objects.

E was the best-performing open source software prover in the 2008 CADE
ATP System Competition (CASC) in the FOF, CNF, and UEQ divisions.  In
the 2011 competition, it won second place in the FOF division, and
placed highly in CNF and UEQ.

%prep
%setup -q -n %{name}

# Set up Fedora CFLAGS and paths
sed -e "s|^EXECPATH = .*|EXECPATH = $RPM_BUILD_ROOT%{_bindir}|" \
    -e "s|^MANPATH = .*|MANPATH = $RPM_BUILD_ROOT%{_mandir}/man1|" \
    -e "s|^CFLAGS.*|CFLAGS = $RPM_OPT_FLAGS -std=gnu99 \\\\|" \
    -i Makefile.vars
sed -i "s|^EXECPATH=.*|EXECPATH=%{_bindir}|" PROVER/eproof PROVER/eproof_ram

# Fix the character encoding of one file
iconv -f ISO8859-1 -t UTF-8 DOC/E-REMARKS > DOC/E-REMARKS.utf8
touch -r DOC/E-REMARKS DOC/E-REMARKS.utf8
mv -f DOC/E-REMARKS.utf8 DOC/E-REMARKS

# Preserve timestamps when installing
sed -i 's|cp \$1|cp -p $1|' development_tools/e_install


%build
# smp_mflags causes unwelcome races, so we will not use it
make remake
make man

%install
make install

%check
./PROVER/eprover -s --tptp-in EXAMPLE_PROBLEMS/TPTP/SYN310-1+rm_eq_rstfp.tptp | tail -1 > test-results
echo "# SZS status Unsatisfiable" > test-expected-results
diff test-results test-expected-results


%files
%doc README
%doc COPYING
%doc DOC/bug_reporting
%doc DOC/clib.ps
%doc DOC/CREDITS
%doc DOC/E-1.4pre.html
%doc DOC/eprover.pdf
%doc DOC/E-REMARKS
%doc DOC/E-REMARKS.english
%doc DOC/grammar.txt
%doc DOC/NEWS
%doc DOC/sample_proofs.html
%doc DOC/sample_proofs_tstp.html
%doc DOC/TODO
%doc DOC/TSTP_Syntax.txt
%doc DOC/WISHLIST
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.8.001-3
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 1.8.001-2
- 为 Magic 3.0 重建

* Tue Sep  3 2013 Jerry James <loganjerry@gmail.com> - 1.8.001-1
- New upstream version

* Mon Jul 29 2013 Jerry James <loganjerry@gmail.com> - 1.8-1
- New upstream version
- Drop now unneeded -alias patch

* Mon Mar 25 2013 Jerry James <loganjerry@gmail.com> - 1.7-1
- New upstream release

* Wed Feb 13 2013 Jerry James <loganjerry@gmail.com> - 1.6-2
- Add tex(supertabular.sty) BR due to TeXLive 2012 changes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug  6 2012 Jerry James <loganjerry@gmail.com> - 1.6-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Jerry James <loganjerry@gmail.com> - 1.5-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jan  7 2012 Jerry James <loganjerry@gamil.com> - 1.4-2
- Rebuild for GCC 4.7

* Mon Aug 22 2011 Jerry James <loganjerry@gmail.com> - 1.4-1
- New upstream release
- Rebuild man pages with newer version of help2man
- Use the Makefile's install target instead of rolling our own

* Sat Jul  2 2011 Jerry James <loganjerry@gmail.com> - 1.3-1
- New upstream release

* Tue Jun 21 2011 Jerry James <loganjerry@gmail.com> - 1.2.001-1
- New upstream release
- Now dual-licensed: GPLv2+ or LGPLv2+
- Drop unnecessary spec file elements (BuildRoot, etc.)
- Use virtual provides for the BRs instead of files
- Install the man pages

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 22 2008 David A. Wheeler <dwheeler at, dwheeler.com> 1.0.002-3
- Work around local tags

* Mon Dec 22 2008 David A. Wheeler <dwheeler at, dwheeler.com> 1.0.002-2
- Repaired for python2 variations (different releases have different versions
  of python2)

* Mon Dec 22 2008 David A. Wheeler <dwheeler at, dwheeler.com> 1.0.002-1
- Added python2.5 as BuildRequires
- Update to E version 1.0 ("Temi").  This includes...
- Improved eproof script signal handling.
- Fixed a number of warnings with the latest gcc version.
- Updated proof objects to latest SZS ontology.

* Tue Aug 19 2008 David A. Wheeler <dwheeler at, dwheeler.com> 0.999.006-2
- Change executable permissions from 0775 to 0755 
- Use compilation switches (e.g., -O2 instead of pointless -O6, and use -g)
 
* Tue Aug 19 2008 David A. Wheeler <dwheeler at, dwheeler.com> 0.999.006-1
- Initial package

