# Generated from websocket-driver-0.3.4.gem by gem2rpm -*- rpm-spec -*-
%global gem_name websocket-driver

Name: rubygem-%{gem_name}
Version: 0.3.4
Release: 6%{?dist}
Summary: WebSocket protocol handler with pluggable I/O
Group: Development/Languages
License: MIT
URL: http://github.com/faye/websocket-driver-ruby
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/faye/websocket-driver-ruby.git
# cd websocket-driver-ruby && git checkout 0.3.4
# tar czvf websocket-driver-ruby-0.3.4-tests.tgz spec/
Source1: websocket-driver-ruby-0.3.4-tests.tgz
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby-devel
BuildRequires: rubygem(eventmachine)
BuildRequires: rubygem(rake-compiler)
BuildRequires: rubygem(rspec) < 3.0

%if 0%{?fedora} <= 20
Requires: ruby(release)
Requires: ruby(rubygems) 
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
This module provides a complete implementation of the WebSocket protocols that
can be hooked up to any TCP library. It aims to simplify things by decoupling
the protocol details from the I/O layer, such that users only need to implement
code to stream data in and out of it without needing to know anything about how
the protocol actually works. Think of it as a complete WebSocket system with
pluggable I/O.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}/lib/

mv %{buildroot}%{gem_instdir}/ext/%{gem_name}/websocket_mask.so \
   %{buildroot}%{gem_extdir_mri}/lib

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
pushd .%{gem_instdir}
tar xf %{SOURCE1}
# Bundler
sed -i -e '2d' examples/tcp_server.rb
sed -i -e '2d' spec/spec_helper.rb
rspec2 -I$(dirs +1)%{gem_extdir_mri} spec
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_extdir_mri}
%exclude %{gem_cache}
%doc %{gem_instdir}/README.md
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/examples

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 0.3.4-6
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 0.3.4-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.3.4-4
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jan 18 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.3.4-2
- Rebuild for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Tue Jul 15 2014 Josef Stribny <jstribny@redhat.com> - 0.3.4-1
- Initial package
