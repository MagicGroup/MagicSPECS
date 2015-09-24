%global gem_name Ascii85
%if 0%{?rhel} == 6
%global gem_dir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{version}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{version}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{version}
%endif

Summary: Methods to encode/decode Adobe's binary-to-text encoding of the same name
Name: rubygem-%{gem_name}
Version: 1.0.2
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://ascii85.rubyforge.org/
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem
#retrieved from http://rubyforge.org/tracker/index.php?func=detail&aid=29377&group_id=7826&atid=30313
Source1: ascii85.1.pod.tgz 

%if 0%{?rhel} == 6
Requires: ruby(abi) = 1.8
%else
Requires: ruby(release)
%endif
%if 0%{?fedora}
BuildRequires: rubygems-devel
%endif
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}
BuildRequires: %{_bindir}/pod2man
BuildRequires: rubygem(minitest)
%description
Ascii85 is a simple gem that provides methods for encoding/decoding Adobe's
binary-to-text encoding of the same name.

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
tar zxvf %{SOURCE1}

%build

# without -KU, it fails with: invalid byte sequence in US-ASCII
RUBYOPT="-KU" gem build %{gem_name}.gemspec

%gem_install

pod2man --center "" --release "" --name ASCII85 --utf8 --section=1 ascii85.1.pod ascii85.1

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

mv %{buildroot}%{gem_instdir}/{History.txt,README.rdoc} ./
rm -rf %{buildroot}%{gem_instdir}/{.gitignore,.gemtest}
rm -f %{buildroot}%{gem_instdir}/%{gem_name}.gemspec
rm -rf %{buildroot}%{gem_instdir}/.yardoc

install -D -m 644 ascii85.1 %{buildroot}%{_mandir}/man1/ascii85.1

%check
pushd ./%{gem_instdir}
ruby -I./lib spec/lib/ascii85_spec.rb
popd


%files
%{_bindir}/ascii85
%dir %{gem_instdir}
%{gem_instdir}/lib
%{gem_instdir}/bin
%exclude %{gem_cache}
%{gem_spec}
%{_mandir}/man1/ascii85.1*
%doc %{gem_instdir}/LICENSE

%files doc
%doc History.txt README.rdoc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Miroslav Suchý <msuchy@redhat.com> - 1.0.2-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.2-1
- 874854 - rebase to Ascii85-1.0.2.gem (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-7
- add rubygem to BR (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-6
- do not run test on rhel, where is no rspec (msuchy@redhat.com)

* Fri Aug 24 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-5
- 850469 - in BR do s/perl/pod2man/ (msuchy@redhat.com)
- 850469 - set man generation flags (msuchy@redhat.com)

* Thu Aug 23 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-4
- 850469 do not delete %%{gem_instdir}/bin (msuchy@redhat.com)
- 850469 - pass -KU option better way (msuchy@redhat.com)
- 850469 - edit test suite (msuchy@redhat.com)
- add rspec to BR (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-3
- add ascii85.1.pod.tgz (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-2
- tune spec for Fedora (msuchy@redhat.com)

* Tue Aug 21 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.1-1
- new package built with tito

