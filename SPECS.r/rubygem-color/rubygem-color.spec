# Generated from color-1.4.1.gem by gem2rpm -*- rpm-spec -*-
%global gem_name color

Name: rubygem-%{gem_name}
Version: 1.7.1
Release: 3%{?dist}
Summary: Colour management with Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/halostatue/color
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
BuildRequires: rubygem(minitest)
BuildArch: noarch

%description
Color is a Ruby library to provide basic RGB, CMYK, HSL, and other colourspace
manipulation support to applications that require it. It also provides 152
named RGB colours (184 with spelling variations) that are commonly supported
in HTML, SVG, and X11 applications. A technique for generating monochromatic
contrasting palettes is also included.

The Color library performs purely mathematical manipulation of the colours
based on colour theory without reference to colour profiles (such as sRGB or
Adobe RGB). For most purposes, when working with RGB and HSL colour spaces,
this won't matter. Absolute colour spaces (like CIE L*a*b* and XYZ) and cannot
be reliably converted to relative colour spaces (like RGB) without colour
profiles.


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

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
ruby -Ilib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)'
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/Licence.rdoc
%exclude %{gem_instdir}/.*
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Contributing.rdoc
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/Manifest.txt
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%{gem_instdir}/test

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.7.1-3
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.7.1-2
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Vít Ondruch <vondruch@redhat.com> - 1.7.1-1
- Update to Color 1.7.1.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 12 2014 Vít Ondruch <vondruch@redhat.com> - 1.6-1
- Update to Color 1.6.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-4
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-2
- Alter the specfile to build on el6, too.

* Tue Nov 13 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.1-1
- Initial package
