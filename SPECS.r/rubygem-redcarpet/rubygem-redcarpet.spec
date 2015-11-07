%global gem_name redcarpet

Name: rubygem-%{gem_name}
Version: 3.3.2
Release: 3%{?dist}
Summary: A fast, safe and extensible Markdown to (X)HTML parser
Group: Development/Languages
# https://github.com/vmg/redcarpet/issues/502
License: MIT and ISC
URL: http://github.com/vmg/redcarpet
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(test-unit)

%description
A fast, safe and extensible Markdown to (X)HTML parser.


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

# https://github.com/vmg/redcarpet/pull/503
chmod a-x .%{gem_instdir}/ext/redcarpet/html.c

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/redcarpet

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}
RUBYOPT=-Ilib:$(dirs +1)%{gem_extdir_mri}:test ruby -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{_bindir}/redcarpet
%{gem_instdir}/bin
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}
%license %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.markdown

%files doc
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/test
%{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_docdir}


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 3.3.2-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.3.2-2
- 为 Magic 3.0 重建

* Wed Jul 08 2015 Vít Ondruch <vondruch@redhat.com> - 3.3.2-1
- Update to Redcarpet 3.3.2.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Vít Ondruch <vondruch@redhat.com> - 2.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Vít Ondruch <vondruch@redhat.com> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Josef Stribny <jstribny@redhat.com> - 2.1.1-7
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-4
- Removing conditionals

* Mon May 21 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-3
- Adding newer rdoc build requires to fix rpmdiff issue

* Fri May 18 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-2
- Cleaning up spec to remove patch and rake testing dependency

* Thu Apr 26 2012 Matt Hicks <mhicks@redhat.com> - 2.1.1-1
- Initial package
