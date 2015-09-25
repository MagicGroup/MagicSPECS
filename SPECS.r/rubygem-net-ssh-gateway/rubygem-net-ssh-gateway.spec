# Generated from net-ssh-gateway-1.1.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name net-ssh-gateway

Summary: A simple library to assist in establishing tunneled Net::SSH connections
Name: rubygem-%{gem_name}
Version: 1.2.0
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/net-ssh/net-scp
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(net-ssh) >= 2.6.5
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(test-unit)
BuildArch: noarch

%description
A simple library to assist in establishing tunneled Net::SSH connections


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


%check
pushd .%{gem_instdir}
# Fix Mocha 1.x compatibility.
# https://github.com/net-ssh/net-ssh-gateway/pull/5
sed -i 's|mocha|mocha/setup|' test/gateway_test.rb

ruby -Ilib -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Manifest
%{gem_instdir}/Rakefile
%{gem_instdir}/net-ssh-gateway.gemspec
%{gem_instdir}/gem-public_cert.pem
%{gem_instdir}/setup.rb
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/CHANGES.txt
%{gem_instdir}/test


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.2.0-6
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 1.2.0-4
- Fix FTBFS in Rawhide (rhbz#1107178).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.0-1
- Update to net-ssh-gateway 1.2.0.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.0-8
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.0-5
- Fix broken dependency.

* Tue Jan 31 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 06 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.0-2
- Removed unnecessary setup.rb.

* Thu May 26 2011 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Initial package
