# Generated from paranoia-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name paranoia

Summary: Cleaner re-implementation of acts_as_paranoid (ActiveRecord soft-delete plugin)
Name: rubygem-%{gem_name}
Version: 2.0.2
Release: 5%{?dist}
Group: Development/Languages
License: MIT
URL: http://rubygems.org/gems/paranoia
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# As of rails 4.0.4, touch fires after_commit callback - fixed test.
# https://github.com/radar/paranoia/commit/563c6cbba22c9e58ad6186c18d04033237ea961b
Patch0: rubygem-paranoia-2.0.2-touch-fires-after-commit-callback-fixed-test.patch
BuildRequires: ruby(release)
BuildRequires: ruby 
BuildRequires: rubygems-devel
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(activerecord)
BuildArch: noarch

%description
Paranoia is a re-implementation of acts_as_paranoid
(http://github.com/technoweenie/acts_as_paranoid) for Rails 3, using much,
much, much less code. You would use either plugin / gem if you wished that
when you called 'destroy' on an Active Record object that it didn't actually
destroy it, but just "hid" the record. Paranoia does this by setting a
'deleted_at' field to the current time when you 'destroy' a record, and hides
it by scoping all queries on your model to only include records which do not
have a 'deleted_at' field.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build

%check
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./test/*_test.rb", &method(:require)'
popd

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/
pushd %{buildroot}%{gem_instdir}
rm -f .gitignore
rm -rf test
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/.*
%{gem_spec}
%{gem_instdir}/README.md
%{gem_instdir}/LICENSE

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/paranoia.gemspec
%{gem_instdir}/Gemfile

%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.2-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.2-4
- 为 Magic 3.0 重建

* Tue Jul 29 2014 Vít Ondruch <vondruch@redhat.com> - 2.0.2-3
- Fix FTBFS in Rawhide (hrbz#1107191).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 03 2014 Steve Linabery <slinaber@redhat.com> - 2.0.2-1
- Update to paranoia 2.0.2

* Mon Aug 19 2013 Josef Stribny <jstribny@redhat.com> - 2.0.0-1
- Update to paranoia 2.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 12 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Steve Linabery <slinaber@redhat.com> - 1.1.0-3
- simplify check section

* Mon Apr 30 2012 Steve Linabery <slinaber@redhat.com> - 1.1.0-2
- Add BuildRequires for test suite execution
- Add test suite execution in check section

* Thu Apr 19 2012 Steve Linabery <slinaber@redhat.com> - 1.1.0-1
- Initial package
- remove mildly profane technical term from gemspec
