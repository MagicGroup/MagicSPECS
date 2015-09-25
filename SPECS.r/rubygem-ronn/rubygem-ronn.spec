# Missing BR rubygem(contest), necessary for running the test suite in %%check.
%global gem_name ronn

Name:           rubygem-%{gem_name}
Version:        0.7.3
Release:        8%{?dist}
Summary:        Manual authoring tool

Group:          Development/Tools
License:        MIT
URL:            https://github.com/rtomayko/ronn
Source0:        http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildArch:      noarch
BuildRequires:  rubygems-devel
Requires:       rubygem(hpricot) rubygem(rdiscount) rubygem(mustache) rubygems groff-base

%if 0%{?fedora} >= 19
Requires: ruby(release)
%else
Requires: ruby(abi) >= 1.9.1
%endif

%description
Ronn builds manuals. It converts simple, human readable text files to
roff for terminal display, and also to HTML for the web.

The source format includes all of Markdown but has a more rigid structure and
syntax extensions for features commonly found in man pages (definition lists,
link notation, etc.). The ronn-format(7) manual page defines the format in
detail.

%package doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildArch:      noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
mkdir -p .%{gem_dir}
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
chmod -x %{buildroot}%{gem_instdir}/lib/%{gem_name}.rb

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

# Man pages.
install -D -m 0644 %{buildroot}%{gem_instdir}/man/%{gem_name}.1 %{buildroot}/%{_mandir}/man1/%{gem_name}.1
install -D -m 0644 %{buildroot}%{gem_instdir}/man/%{gem_name}-format.7 %{buildroot}/%{_mandir}/man7/%{gem_name}-format.7

rm -rf %{buildroot}%{gem_instdir}/{INSTALLING,Rakefile,test,man,ronn.gemspec,config.ru}

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/[A-Z]*
%{gem_instdir}/bin
%{gem_libdir}
%{gem_cache}
%{gem_spec}
%{_bindir}/%{gem_name}
%{_mandir}/man1/%{gem_name}.1*
%{_mandir}/man7/%{gem_name}-format.7*

%files doc
%{gem_docdir}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.7.3-8
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 4 2013 Ricky Elrod <codeblock@fedoraproject.org> 0.7.3-4
- Add groff-base Requires.
- Nuke a Requires of the base package from the -doc subpackage.
- Fix Requires for F18-, make it be >= 1.9.1.

* Fri Apr 5 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-3
- Fix Requires so the package works on F18- and F19+.
- Fix what is marked as doc.
- Remove some extra files from the gem_instdir which are only needed for building.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-2
- Move things into a doc subpackage.
- Fix BuildRequires.
- Document why the test suite isn't running.
- Make some things that don't need to be installed, not install.
- Mark some files as doc files.

* Wed Apr 3 2013 Ricky Elrod <codeblock@fedoraproject.org> - 0.7.3-1
- Initial build.
