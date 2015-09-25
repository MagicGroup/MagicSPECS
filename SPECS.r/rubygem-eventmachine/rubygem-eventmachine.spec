%global gem_name eventmachine

# This enables to run full test suite, where network connection is available.
# However, it must be disabled for Koji build.
%{!?network: %global network 0}

Summary:    Ruby/EventMachine library
Name:       rubygem-%{gem_name}
Version:    1.0.6
Release:    4%{?dist}
Group:      Development/Languages
License:    GPLv2 or Ruby
URL:        http://rubyeventmachine.com
Source0:    http://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(test-unit)
# Enables SSL support.
BuildRequires: openssl-devel

%description
EventMachine implements a fast, single-threaded engine for arbitrary network
communications. It's extremely easy to use in Ruby. EventMachine wraps all
interactions with IP sockets, allowing programs to concentrate on the
implementation of network protocols. It can be used to create both network
servers and clients. To create a server or client, a Ruby program only needs
to specify the IP address and port, and provide a Module that implements the
communications protocol. Implementations of several standard network protocols
are provided with the package, primarily to serve as examples. The real goal
of EventMachine is to enable programs to easily interface with other programs
using TCP/IP, especially if custom protocols are required.

%package doc
Summary: Documentation for %{name}
Group: Documentation
BuildArch: noarch

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.


%prep
%setup -q -T -c
%gem_install -n %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/* %{buildroot}%{gem_extdir_mri}/

# Prevent dangling symlink in -debuginfo.
rm -rf %{buildroot}%{gem_instdir}/ext

%check
pushd .%{gem_instdir}

# test_localhost(TestResolver) fails.
# https://github.com/eventmachine/eventmachine/issues/579
sed -i '/test_localhost/,/^  end$/ s/^/#/' tests/test_resolver.rb
# test_dispatch_completion(TestThreadedResource) fails randomly.
# https://github.com/eventmachine/eventmachine/issues/580
sed -i '/test_dispatch_completion/,/^  end$/ s/^/#/' tests/test_threaded_resource.rb

# Unfortunatelly test_a exists in more test cases.
ruby -Ilib:$(dirs +1)%{gem_extdir_mri}:.:tests -e "Dir.glob 'tests/test_*.rb', &method(:require)" -- \
%if 0%{network} < 1
  --ignore-name=/^test_bind_connect$/ \
  --ignore-name=/^test_get_sock_opt$/ \
  --ignore-name=/^test_cookie$/ \
  --ignore-name=/^test_http_client$/ \
  --ignore-name=/^test_http_client_1$/ \
  --ignore-name=/^test_http_client_2$/ \
  --ignore-name=/^test_version_1_0$/ \
  --ignore-name=/^test_get$/ \
  --ignore-name=/^test_get_pipeline$/ \
  --ignore-name=/^test_https_get$/ \
  --ignore-name=/^test_idle_time$/ \
  --ignore-name=/^test_a$/ \
  --ignore-name=/^test_a_pair$/ \
  --ignore-name=/^test_bad_host$/ \
  --ignore-name=/^test_failure_timer_cleanup$/ \
  --ignore-name=/^test_timer_cleanup$/ \
  --ignore-name=/^test_set_sock_opt$/ \
  --ignore-name=/^test_connect_timeout$/ \
%endif

popd

%files
%doc %{gem_instdir}/GNU
%doc %{gem_instdir}/LICENSE
%dir %{gem_instdir}/
%exclude %{gem_instdir}/.*
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs
%{gem_instdir}/eventmachine.gemspec
%{gem_instdir}/examples
# TODO: Hmm, we can build also JRuby bindigs.
%{gem_instdir}/java
%{gem_instdir}/rakelib
%{gem_instdir}/tests

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.0.6-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 04 2015 Vít Ondruch <vondruch@redhat.com> - 1.0.6-1
- Update to EventMachine 1.0.6.

* Sat Jan 17 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.0.4-1
- 1.0.4 (https://github.com/eventmachine/eventmachine/issues/495)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 11 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Update to eventmachine 1.0.3.

* Thu Feb 28 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.1-1
- Update to eventmachine 1.0.1.
- Enable SSL support.

* Wed Feb 27 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.0-1
- Update to eventmachine 1.0.0.

* Wed Feb 27 2013 Vít Ondruch <vondruch@redhat.com> - 0.12.10-9
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 19 2012 Vít Ondruch <vondruch@redhat.com> - 0.12.10-6
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-3
- More review fixes

* Sun Jan 31 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 0.12.10-2
- Review fixes (#556433)

* Mon Jan 18 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> - 0.12.10-1
- Initial package
