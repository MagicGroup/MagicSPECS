%global gem_name stomp

Summary: Ruby client for the Stomp messaging protocol
Name: rubygem-%{gem_name}
Version: 1.3.4
Release: 5%{?dist}
Group: Development/Languages
License: ASL 2.0
URL: http://stomp.codehaus.org/
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: stomp-1.3.4-stub-deprecate.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
%endif
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec) < 3
BuildArch: noarch
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Ruby client for the Stomp messaging protocol

%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}
%patch0 -p1

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x


%clean
rm -rf %{buildroot}

%check
pushd %{buildroot}/%{gem_instdir}
%if 0%{?fc19} || 0%{?fc20} || 0%{?fc21} || 0%{?el7}
rspec  -Ilib spec
%else
rspec2 -Ilib spec
%endif
popd

%files
%dir %{gem_instdir}
%{_bindir}/catstomp
%{_bindir}/stompcat
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/stomp.gemspec
%{gem_spec}


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CHANGELOG.rdoc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/spec
%doc %{gem_instdir}/notes
%doc %{gem_instdir}/examples/client11_ex1.rb
%doc %{gem_instdir}/examples/client11_putget1.rb
%doc %{gem_instdir}/examples/conn11_ex1.rb
%doc %{gem_instdir}/examples/conn11_ex2.rb
%doc %{gem_instdir}/examples/conn11_hb1.rb
%doc %{gem_instdir}/examples/consumer.rb
%doc %{gem_instdir}/examples/examplogger.rb
%doc %{gem_instdir}/examples/get11conn_ex1.rb
%doc %{gem_instdir}/examples/get11conn_ex2.rb
%doc %{gem_instdir}/examples/logexamp.rb
%doc %{gem_instdir}/examples/logexamp_ssl.rb
%doc %{gem_instdir}/examples/publisher.rb
%doc %{gem_instdir}/examples/put11conn_ex1.rb
%doc %{gem_instdir}/examples/putget11_rh1.rb
%doc %{gem_instdir}/examples/ssl_ctxoptions.rb
%doc %{gem_instdir}/examples/ssl_newparm.rb
%doc %{gem_instdir}/examples/ssl_uc1.rb
%doc %{gem_instdir}/examples/ssl_uc1_ciphers.rb
%doc %{gem_instdir}/examples/ssl_uc2.rb
%doc %{gem_instdir}/examples/ssl_uc2_ciphers.rb
%doc %{gem_instdir}/examples/ssl_uc3.rb
%doc %{gem_instdir}/examples/ssl_uc3_ciphers.rb
%doc %{gem_instdir}/examples/ssl_uc4.rb
%doc %{gem_instdir}/examples/ssl_uc4_ciphers.rb
%doc %{gem_instdir}/examples/ssl_ucx_default_ciphers.rb
%doc %{gem_instdir}/examples/stomp11_common.rb
%doc %{gem_instdir}/examples/topic_consumer.rb
%doc %{gem_instdir}/examples/topic_publisher.rb
%doc %{gem_instdir}/test/test_anonymous.rb
%doc %{gem_instdir}/test/test_client.rb
%doc %{gem_instdir}/test/test_codec.rb
%doc %{gem_instdir}/test/test_connection.rb
%doc %{gem_instdir}/test/test_connection1p.rb
%doc %{gem_instdir}/test/test_helper.rb
%doc %{gem_instdir}/test/test_message.rb
%doc %{gem_instdir}/test/test_ssl.rb
%doc %{gem_instdir}/test/test_urlogin.rb
%doc %{gem_instdir}/test/tlogger.rb



%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.3.4-5
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.3.4-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Steve Traylen  <steve.traylen@cern.ch> - 1.3.4-2
- Force rspec 2 tests.

* Wed Mar 11 2015 Steve Traylen  <steve.traylen@cern.ch> - 1.3.4-1
- Upstream 1.3.4 release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.8-2
- BR: rubygem(rspec), not rubygem(rspec-core).

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.8-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Updated to version 1.2.8.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Michael Stahnke <stahnma@puppetlabs.com> - 1.2.2-1
- Update to 1.2.2

* Fri Feb 03 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.9-3
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Michael Stahnke <stahnma@puppetlabs.com> -  1.19-1
- New version from upstream

* Fri Mar 18 2011 <stahnma@fedoraproject.org> - 1.1.8-1
- New version from upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 05 2010 Michael Stahnke <stahnma@fedoraproject.org> - 1.1.6-1
- Initial Package
