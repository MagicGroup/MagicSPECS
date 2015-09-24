%if 0%{?el6}
%global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"]')
%endif

# Generated from curb-0.7.7.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name curb

Summary: Ruby libcurl bindings
Name: rubygem-%{gem_name}
Version: 0.8.8
Release: 2%{?dist}
Group: Development/Languages
License: Ruby
URL: https://github.com/taf2/curb
Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0: curb-disable-network-lookup-test.patch

%if 0%{?el6}
Requires: ruby(abi) = 1.8 
Requires: ruby(rubygems)
%endif
%if 0%{?fc19} || 0%{?fc20} || 0%{?el7}
Requires: ruby(release)
Requires: ruby(rubygems)
%endif

%if 0%{?el6}
BuildRequires: ruby(abi) = 1.8 
%else
BuildRequires: ruby(release)
%endif
BuildRequires: rubygems-devel
# minitest 5 requires some migration work
# https://www.mail-archive.com/ruby-sig@lists.fedoraproject.org/msg01474.html
BuildRequires: rubygem(minitest) < 5
BuildRequires: ruby-devel
BuildRequires: libcurl-devel
%if 0%{?fc19} || 0%{?fc20} || 0%{?el6} || 0%{?el7}
Provides: rubygem(%{gem_name}) = %{version}
%endif

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}


%description doc
Documentation for %{name}

%description
Curb (probably CUrl-RuBy or something) provides Ruby-language bindings for the
libcurl(3), a fully-featured client-side URL transfer library. cURL and
libcurl live at http://curl.haxx.se/


%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

# Disable due to Curl::Err::HostResolutionError, which is cause probably by
# missing network access on Koji.
%patch0 -p1

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -pa .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%%if 0%{?el6}
mkdir -p  %{buildroot}%{ruby_sitearch}
mv %{buildroot}%{gem_instdir}/lib/curb_core.so %{buildroot}/%{ruby_sitearch}/curb_core.so
%else
mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
%endif

# Prevent dangling symlink in -debuginfo (rhbz#878863).
rm -rf %{buildroot}%{gem_instdir}/ext/

%check
%if ! 0%{?el6}
pushd .%{gem_instdir}
ruby -e 'Dir.glob "./tests/tx_*.rb", &method(:require)'
popd
%endif

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/tests
%exclude %{gem_instdir}/Rakefile
%exclude %{gem_instdir}/doc.rb
%if 0%{?el6}
%exclude %{gem_instdir}/.require_paths
%endif
%if 0%{?el6}
%{ruby_sitearch}/curb_core.so
%else
%{gem_extdir_mri}
%endif
%exclude %{gem_cache}
%{gem_spec}


%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.markdown


%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 2 2015 Steve Traylen <steve.traylen@cern.ch> - 0.8.8-1
- Upstream 0.8.8

* Mon Mar 23 2015 Steve Traylen <steve.traylen@cern.ch> - 0.8.7-1
- Upstream 0.8.7

* Thu Jan 15 2015 Vít Ondruch <vondruch@redhat.com> - 0.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Ruby_2.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 4 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.6-1
- Upstream 0.8.6, update to new ruby guidelines.

* Tue Jun 17 2014 Vít Ondruch <vondruch@redhat.com> - 0.8.5-3
- Place extension into correct location.
- Prevent dangling symlinks in -debuginfo.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.5-1
- Update to 0.8.5, avoid minitest-5 for now.

* Wed Apr 9 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.4-2
- Now really works on EPEL6.

* Tue Mar 11 2014 Steve Traylen <steve.traylen@cern.ch> - 0.8.4-1
- Update to curb 0.8.4, fix to latest ruby guidelines.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.8.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Vít Ondruch <vondruch@redhat.com> - 0.8.3-1
- Update to curb 0.8.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 01 2012 Vít Ondruch <vondruch@redhat.com> - 0.7.10-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 25 2011 Shreyank Gupta <sgupta@redhat.com> - 0.7.10-2
- not excluding .require_paths

* Fri Feb 25 2011 Shreyank Gupta <sgupta@redhat.com> - 0.7.10-1
- New upstream 0.7.10

* Wed Jul 21 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-4
- Remove unneeded .require_paths file

* Tue Jul 20 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-3
- Remove unneeded .o and .so files from ext/ directory
- No rake test for ppc64

* Mon Jul 19 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-2
- Install gem file under %%gemdir and then copy to %%buildroot
- Moving .so to %%ruby_sitearch
- BuildRequires: rubygem(rake)

* Fri Jul 02 2010 Shreyank Gupta <sgupta@redhat.com> - 0.7.7.1-1
- Initial package
