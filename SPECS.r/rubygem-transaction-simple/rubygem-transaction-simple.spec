%global gem_name transaction-simple
%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

Summary: Simple object transaction support for Ruby
Name: rubygem-%{gem_name}
Version: 1.4.0.2
Release: 11%{?dist}
Group: Development/Languages
License: MIT
URL: http://trans-simple.rubyforge.org/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
# Use minitest 5
# https://github.com/halostatue/transaction-simple/pull/5
Patch0: rubygem-transaction-simple-minitest5.patch
Requires: rubygems
%if 0%{?rhel} == 6
Requires: ruby(abi) = 1.8
%else
%if 0%{?fedora} >= 19
Requires: ruby(release)
%else
Requires: ruby(release)
%endif
%endif
%if 0%{?fedora}
BuildRequires: rubygems-devel
%endif
BuildRequires: rubygems
%if 0%{?fedora} >= 20
BuildRequires: rubygem(minitest) >= 5.0.0
%else
BuildRequires: rubygem(minitest)
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Transaction::Simple provides a generic way to add active transaction support
to objects. The transaction methods added by this module will work with most
objects, excluding those that cannot be Marshal-ed (bindings, procedure
objects, IO instances, or singleton objects).

%package doc
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Summary:    Documentation for rubygem-%{gem_name}

%description doc
This package contains documentation for rubygem-%{gem_name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
sed -i '/s.cert_chain = nil/d' %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%if 0%{?rhel} == 6
%gem_install
%else
%gem_install
%endif

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
mv %{buildroot}%{gem_instdir}/{History.rdoc,Licence.rdoc,README.rdoc,Manifest.txt} ./
rm -rf %{buildroot}%{gem_instdir}/.yardoc
rm %{buildroot}%{gem_instdir}/.gemtest
chmod a-x %{buildroot}%{gem_instdir}/test/test_broken_graph.rb

%check
%if 0%{?fedora} >= 20
cat %PATCH0 | patch -p1
ruby -Ilib -rminitest/autorun -e "Dir.glob './test/test_*.rb', &method(:require)"
%else
testrb -Ilib test/test_*.rb
%endif

%files
%doc Licence.rdoc
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}
#https://github.com/halostatue/transaction-simple/issues/4
%exclude %{gem_instdir}/research

%files doc
%doc History.rdoc README.rdoc Manifest.txt
%doc %{gem_docdir}
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.0.2-11
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jul 07 2014 Josef Stribny <jstribny@redhat.com> - 1.4.0.2-9
- Fix tests for minitest 5

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 1.4.0.2-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 1.4.0.2-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0.2-3
- 847457 - test script do not have shebang anymore (msuchy@redhat.com)
- 847457 - home page of transaction-simple changed (msuchy@redhat.com)
- 847457 - remove dot files consistently (msuchy@redhat.com)

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0.2-2
- fix changes after rebase (msuchy@redhat.com)
- setup.rb do not exist anymore (msuchy@redhat.com)

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0.2-1
- rebase to transaction-simple 1.4.0.2 (msuchy@redhat.com)
- 847457 - drop cert_chain completly (msuchy@redhat.com)
- 847457 - set executable bit on scripts (msuchy@redhat.com)
- 847457 - mark gem_docdir as as %%doc (msuchy@redhat.com)
- 847457 - remove CONFIGURE_ARGS (msuchy@redhat.com)
- 847457 - move some files to -doc package and exclude gem_cache
  (msuchy@redhat.com)
- 847457 - gem hoe is not needed (msuchy@redhat.com)
- 847457 - use global instead of define (msuchy@redhat.com)

* Sat Aug 11 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0-8
- change license to MIT (msuchy@redhat.com)
- use test suite (msuchy@redhat.com)
- fix filelist (msuchy@redhat.com)
- remove yardoc (msuchy@redhat.com)
- wrap description to 80 chars (msuchy@redhat.com)
- use macros (msuchy@redhat.com)
- buildroot is not needed (msuchy@redhat.com)
- mv transaction-simple.spec rubygem-transaction-simple.spec
  (msuchy@redhat.com)

* Wed Jul 04 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0-7
- cert_chain could not be nil (msuchy@redhat.com)

* Wed Jul 04 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0-6
- edit spec for Fedora 17 (msuchy@redhat.com)

* Fri Jun 29 2012 Miroslav Suchý <msuchy@redhat.com> 1.4.0-5
- rebuild

* Thu Oct 27 2011 Shannon Hughes <shughes@redhat.com> 1.4.0-4
- fixing version to match gem (shughes@redhat.com)

* Thu Oct 27 2011 Shannon Hughes <shughes@redhat.com> 1.4.2-1
- add dep for rubygem-hoe (shughes@redhat.com)

* Thu Oct 27 2011 Shannon Hughes <shughes@redhat.com>
- add dep for rubygem-hoe (shughes@redhat.com)

* Wed Oct 12 2011 Shannon Hughes <shughes@redhat.com> 1.4.0-3
- fixing tag (shughes@redhat.com)
- fix up gem version and tags (shughes@redhat.com)

* Wed Oct 12 2011 Shannon Hughes <shughes@redhat.com>
- fix up gem version and tags (shughes@redhat.com)

* Wed Oct 12 2011 Dmitri Dolguikh <dmitri@redhat.com> 1.4.1-1
- Automatic commit of package [rubygem-transaction-simple] release [1.4.0-2].
  (dmitri@redhat.com)
- bumped up the version on transaction-simple.spec (dmitri@redhat.com)
- fixed transaction-simple spec file (dmitri@redhat.com)
- Automatic commit of package [rubygem-transaction-simple] release [1.4.0-1].
  (dmitri@redhat.com)

* Wed Oct 12 2011 Dmitri Dolguikh <dmitri@redhat.com>
- Automatic commit of package [rubygem-transaction-simple] release [1.4.0-2].
  (dmitri@redhat.com)
- bumped up the version on transaction-simple.spec (dmitri@redhat.com)
- fixed transaction-simple spec file (dmitri@redhat.com)
- Automatic commit of package [rubygem-transaction-simple] release [1.4.0-1].
  (dmitri@redhat.com)

* Tue Oct 11 2011 Dmitri Dolguikh <dmitri@redhat.com> 1.4.0-2
- bumped up the version on transaction-simple.spec (dmitri@redhat.com)
- fixed transaction-simple spec file (dmitri@redhat.com)

* Tue Oct 11 2011 Dmitri Dolguikh <dmitri@redhat.com>
- fixed transaction-simple spec file (dmitri@redhat.com)

* Tue Oct 11 2011 Dmitri Dolguikh <dmitri@redhat.com> 1.4.0-1
- new package built with tito

* Tue Oct 11 2011  <wb@killing-time.appliedlogic.ca> - 1.4.0-1
- Initial package
