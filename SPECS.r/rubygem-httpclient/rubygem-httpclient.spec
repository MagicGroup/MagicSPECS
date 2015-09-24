%global gem_name httpclient

%global rubyabi 1.8

Summary:        HTTP Client interface for ruby
Name:           rubygem-%{gem_name}
Version:        2.5.1
Release:        4%{?dist}
Group:          Development/Languages
License:        (Ruby or BSD) and Public Domain
URL:            https://github.com/nahi/httpclient
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem
%if 0%{?rhel} <= 6 && 0%{?fedora} <= 18
Requires:       ruby(abi) >= %{rubyabi}
BuildRequires:  rubygem-rdoc
%else
Requires:       ruby(release)
%endif
%if 0%{?rhel} <= 7 && 0%{?fedora} <= 20
BuildRequires:  rubygem(minitest)
%else
BuildRequires:  rubygem(minitest4)
BuildRequires:  rubygem(test-unit)
%endif
BuildRequires:  rubygems-devel
BuildArch:      noarch
%if 0%{?el7} || 0%{?el6}
Provides:      rubygem(%{gem_name}) = %{version}
%endif

%description
an interface to HTTP Client for the ruby language

%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# Remove backup and yardoc files
find %{buildroot}/%{gem_instdir} -type f -name "*~" -delete
rm -rf %{buildroot}%{gem_instdir}/.yardoc

# Fix anything executable that does not have a shebang
for file in `find %{buildroot}/%{gem_instdir} -type f -perm /a+x`; do
    [ -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 644 $file
done

# Find files with a shebang that do not have executable permissions
for file in `find %{buildroot}/%{gem_instdir} -type f ! -perm /a+x -name "*.rb"`; do
    [ ! -z "`head -n 1 $file | grep \"^#!/\"`" ] && chmod -v 755 $file
done

# Find files that have non-standard-executable-perm
find %{buildroot}/%{gem_instdir} -type f -perm /g+wx -exec chmod -v g-w {} \;

# Find files that are not readable
find %{buildroot}/%{gem_instdir} -type f ! -perm /go+r -exec chmod -v go+r {} \;

%check
pushd %{buildroot}%{gem_instdir}
# All the tests in test_auth.rb were being bypassed
#  but on Ruby 1.8, the bypass didn't work and would fail.
# Just remove the file since it was being bypassed anyway.
rm -f test/test_auth.rb
ruby -Ilib -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%{gem_instdir}/bin/
%{gem_instdir}/lib/
%doc %{gem_instdir}/sample
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/test


%changelog
* Tue Jul 21 2015 Troy Dawson <tdawson@redhat.com> - 2.5.1-4
- Changed check from testrb2 to ruby

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.5.1-2
- EPEL6 need rubygem-rdoc

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.5.1-1
- Update to 2.5.1 

* Mon Oct 20 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-3
- Update spec to follow latest guidelines

* Wed Oct 15 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-2
- Fix spec make it build and install on epel7 and older versions of fedora

* Fri Jun 13 2014 Troy Dawson <tdawson@redhat.com> - 2.4.0-1
- Update to latest upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Adam Miller <maxamillion@fedoraproject.org> - 2.3.4.1-1
- Update to latest upstream

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-6
- Fix to make it build/install on F19+

* Thu Feb 28 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-5
- Fix check to work on EPEL6

* Wed Feb 27 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-4
- Set License to (Ruby or BSD) and Public Domain

* Tue Feb 05 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-3
- Fix URL
- Removed line that changed /usr/bin/env to /usr/bin/ruby

* Mon Jan 21 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-2
- Add Check section
- Put docs in own rpm

* Mon Jan 07 2013 Troy Dawson <tdawson@redhat.com> - 2.3.2-1
- Update to 2.3.2
- Change spec to Fedora ruby standards

* Mon Sep 19 2011 Scott Henson <shenson@redhat.com> - 2.2.1-1
- Initial Packaging

