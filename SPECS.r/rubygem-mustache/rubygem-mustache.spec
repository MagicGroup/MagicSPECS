%global gem_name mustache

Name: rubygem-%{gem_name}
Version: 1.0.2
Release: 3%{?dist}
Summary: Mustache is a framework-agnostic way to render logic-free views
Group: Development/Languages
License: MIT
URL: https://github.com/mustache/mustache
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Inspired by ctemplate, Mustache is a framework-agnostic way to render
logic-free views.

As ctemplates says, "It emphasizes separating logic from presentation:
it is impossible to embed application logic in this template
language.

Think of Mustache as a replacement for your views. Instead of views
consisting of ERB or HAML with random helpers and arbitrary logic,
your views are broken into two parts: a Ruby class and an HTML
template.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Install man pages
mkdir -p %{buildroot}%{_mandir}/man5
cp -a .%{gem_instdir}/man/mustache.5 %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man1
cp -a .%{gem_instdir}/man/mustache.1 %{buildroot}%{_mandir}/man1

# Install documentation
cp -a .%{gem_instdir}/man/*.html .

%check
pushd .%{gem_instdir}
# We are not interested in code quality that much.
sed -r -i '/[Cc]ode[Cc]limate/ s/^/#/' test/helper.rb

# UTF8 environment has to be set.
# https://github.com/mustache/mustache/issues/208
LANG=en_US.utf8 ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%doc *.html
%{_bindir}/mustache
%license %{gem_instdir}/LICENSE
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_instdir}/man
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.0.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.2-2
- 为 Magic 3.0 重建

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.2-1
- Update to Mustache 1.0.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 Vít Ondruch <vondruch@redhat.com> - 0.99.5-1
- Update to Mustache 0.99.5.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 04 2013 Vít Ondruch <vondruch@redhat.com> - 0.99.4-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-6
- Fix mustache executable for Ruby 1.9.3 (rhbz#859025).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-4
- Compatibility fixes with older Fedoras and RHELs.
- Add missing .gemspec.

* Fri Jan 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.99.4-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Vít Ondruch <vondruch@redhat.com> - 0.99.4-1
- Update to Mustache 0.99.4
- Dropped optional Sinatra dependency.
- Removed deprecated %%clean section.
- Added man pages.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-4
- Corrected ruby(abi) require

* Mon Nov 8 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-3
- Added README.md, LICENSE with macro doc
- Replaced macro {gemdir}/gems/{gemname}-{version}/ by macro dir {geminstdir}
- Added lib, bin to macro {geminstdir}
- Added subpackage doc with folders: man, test and doc

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-2
- Repair URL Source0
- Remove "Mustache is a" from Summary
- Add Require: rubygem(sinatra)

* Mon Oct 18 2010 Jozef Zigmund <jzigmund@redhat.com> - 0.11.2-1
- Initial package
