# Generated from authlogic-2.1.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name authlogic


Summary: A clean, simple, and unobtrusive ruby authentication solution
Name: rubygem-%{gem_name}
Version: 3.4.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/binarylogic/authlogic
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildRequires: rubygems-devel
BuildRequires: rubygem(activerecord)
BuildRequires: rubygem(bcrypt)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(request_store)
BuildRequires: rubygem(sqlite3)
BuildRequires: rubygem(timecop)
BuildArch: noarch

%description
A clean, simple, and unobtrusive ruby authentication solution.

%package doc
Summary: Authlogic gem documentation
License: MIT
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for rubygem-authlogic

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}


pushd .%{gem_instdir}

# these files shouldn't be here
rm -f %{gem_name}.gemspec .gitignore Gemfile.lock

# zero length file / not used (test suite requires jeweler gem anyways)
rm -f test/session_test/credentials_test.rb
popd


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}


%check
pushd .%{gem_instdir}
# SCrypt is not available in Fedora.
sed -i '/SCrypt/ s/^/#/' \
  test/acts_as_authentic_test/password_test.rb \
  lib/authlogic/crypto_providers.rb
mv test/crypto_provider_test/scrypt_test.rb{,.disabled}

# Use BCryp instead of SCrypt for tests.
sed -i 's/SCrypt/BCrypt/' test/fixtures/users.yml
sed -i '/rw_config(:crypto_provider, CryptoProviders::SCrypt)/ s/SCrypt/BCrypt/' lib/authlogic/acts_as_authentic/password.rb

# Tests needs to be executed in order.
# https://github.com/binarylogic/authlogic/issues/423
ruby -Ilib:test -e 'Dir.glob("./test/**/*_test.rb").sort.each(&method(:require))'
popd


%files
%dir %{gem_instdir}/
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/History
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 3.4.2-2
- 为 Magic 3.0 重建

* Mon Aug 04 2014 Vít Ondruch <vondruch@redhat.com> - 3.4.2-1
- Update to Authlogic 3.4.2.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Vít Ondruch <vondruch@redhat.com> - 3.1.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Mo Morsi <mmorsi@redhat.com> - 3.1.3-1
- Updated to 3.1.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 3.0.3-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Chris Lalancette <clalance@redhat.com> - 3.0.3-1
- Update to upstream 3.0.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 13 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.6-4
- added missing "Requires: %%{name}" needed in docs subpackage

* Tue Oct 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.6-3
- removed patch0 as ruby-debug is now in fedora

* Tue Oct 12 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.6-2
- added bcrypt-ruby and rake BRs
- removed BuildRoot tag
- removed "--no-ri" flag to gem install
- created doc subpackage
- added patch1 to remove jeweler dep which is not needed

* Tue Aug 10 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.6-1
- Updated to version 2.1.6
- Minor cleanup based on feedback
- Added patch0 to remove unused ruby-debug dependency

* Tue Aug 03 2010 Mohammed Morsi <mmorsi@redhat.com> - 2.1.5-1
- Initial package
