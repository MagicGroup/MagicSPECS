%global gem_name ttfunk

Summary: Font Metrics Parser for Prawn
Name: rubygem-%{gem_name}
Version: 1.4.0
Release: 2%{?dist}
Group: Development/Languages
License: GPLv2 or GPLv3 or Ruby
URL: https://github.com/prawnpdf/ttfunk
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: rubygems
Requires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: rubygems
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
TTFunk is a TrueType font parser written in pure ruby.

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

%build

# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

%gem_install
rm -rf ./%{gem_dir}/gems/%{gem_name}-%{version}/.yardoc

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
mv %{buildroot}%{gem_instdir}/{CHANGELOG,COPYING,GPLv2,GPLv3,LICENSE,README.rdoc} ./

%files
%license COPYING GPLv2 GPLv3 LICENSE
%dir %{gem_instdir}
%{gem_instdir}/lib
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc README.rdoc CHANGELOG
%{gem_instdir}/data
%{gem_instdir}/examples
%doc %{gem_docdir}


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.4.0-2
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Miroslav Suchý 1.4.0-1
- rebase to ttfunk-1.4.0

* Tue Feb 11 2014 Miroslav Suchý <msuchy@redhat.com> 1.1.0-1
- new package built with tito

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Josef Stribny <jstribny@redhat.com> - 1.0.3-6
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-4
- 845805 - move CHANGELOG to -doc package (msuchy@redhat.com)

* Thu Aug 16 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-3
- 845805 - move README.rdoc to -doc subpackage (msuchy@redhat.com)
- 845805 - mark gem_docdir as %%doc and exclude gem_cache (msuchy@redhat.com)

* Thu Aug 09 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-2
- fix spec for fedora review (msuchy@redhat.com)

* Sun Aug 05 2012 Miroslav Suchý <msuchy@redhat.com> 1.0.3-1
- new package built with tito

