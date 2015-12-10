# Generated from prawn-0.12.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name prawn
%global mainver 1.0.0
%global release 5
%{?prever:
%global gem_instdir %{gem_dir}/gems/%{gem_name}-%{mainver}%{?prever}
%global gem_docdir %{gem_dir}/doc/%{gem_name}-%{mainver}%{?prever}
%global gem_cache %{gem_dir}/cache/%{gem_name}-%{mainver}%{?prever}.gem
%global gem_spec %{gem_dir}/specifications/%{gem_name}-%{mainver}%{?prever}.gemspec
}

Summary: A fast and nimble PDF generator for Ruby
Name: rubygem-%{gem_name}
Version: 2.0.2
Release: 1%{?dist}
Group: Development/Languages
# afm files are licensed by APAFML, the rest of package is GPLv2 or GPLv3 or Ruby
License: (GPLv2 or GPLv3 or Ruby) and APAFML
URL: http://prawn.majesticseacreature.com
Source0: http://rubygems.org/gems/%{gem_name}-%{version}%{?prever}.gem
# Prawn doesnt include these fonts in the final package
# http://github.com/prawnpdf/prawn/pull/490
Source1: rubygem-prawn-missing-test-fonts.tar
BuildRequires: ruby(release)
BuildRequires: rubygems-devel >= 1.3.6
BuildRequires: rubygem(rspec) < 3
BuildRequires: rubygem(ttfunk) >= 1.4
BuildRequires: rubygem(ttfunk) < 1.5
BuildRequires: rubygem(mocha)
BuildRequires: rubygem(pdf-reader) >= 1.2.0
BuildRequires: rubygem(pdf-reader) < 2.0
BuildRequires: rubygem(pdf-inspector) >= 1.2.0
BuildRequires: rubygem(pdf-inspector) < 1.3.0
BuildRequires: rubygem(pdf-core) >= 0.6.0
BuildRequires: rubygem(pdf-core) < 0.7
BuildArch: noarch

%description
Prawn is a pure Ruby PDF generation library that provides a lot of great
functionality while trying to remain simple and reasonably performant.
Here are some of the important features we provide:

- Vector drawing support, including lines, polygons, curves, ellipses, etc.
- Extensive text rendering support, including flowing text and limited inline
  formatting options.
- Support for both PDF builtin fonts as well as embedded TrueType fonts
- A variety of low level tools for basic layout needs, including a simple
  grid system
- PNG and JPG image embedding, with flexible scaling options
- Reporting tools for rendering complex data tables, with pagination support
- Security features including encryption and password protection
- Tools for rendering repeatable content (i.e headers, footers, and page
  numbers)
- Comprehensive internationalization features, including full support for UTF-8
  based fonts, right-to-left text rendering, fallback font support,
  and extension points for customizable text wrapping.
- Support for PDF outlines for document navigation
- Low level PDF features, allowing users to create custom extensions
  by dropping down all the way to the PDF object tree layer.
  (Mostly useful to those with knowledge of the PDF specification)
- Lots of other stuff!

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n %{gem_name}-%{version}%{?prever}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install -n %{gem_name}-%{version}%{?prever}.gem

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
sed -i '/^require "bundler"/d' ./spec/spec_helper.rb
sed -i '/^Bundler.setup/d' ./spec/spec_helper.rb

# Install missing fonts needed for tests
pushd ./data
tar xzvf %{SOURCE1}
popd
# 2 failures known to upstream, proper fix is unclear
# https://github.com/prawnpdf/prawn/issues/603
rspec2 spec | grep '2 failures, 4 pending'
popd

%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/GPLv2
%doc %{gem_instdir}/GPLv3
%exclude %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/data/fonts/MustRead.html
%{gem_instdir}/data/fonts/*.afm
%exclude %{gem_instdir}/.yardopts

%files doc
%doc %{gem_docdir}
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%doc %{gem_instdir}/manual
%{gem_instdir}/data/pdfs
%{gem_instdir}/data/images
%{gem_instdir}/data/*.txt

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 2.0.2-1
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2.0.2-1
- 为 Magic 3.0 重建

* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.0.2-1
- 为 Magic 3.0 重建

* Mon Aug 24 2015 Josef Stribny <jstribny@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon Jun 22 2015 Josef Stribny <jstribny@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Josef Stribny <jstribny@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Mon Jun 23 2014 Josef Stribny <jstribny@redhat.com> - 1.0.0-1
- Update to final 1.0.0 version

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.7.rc2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 06 2014 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.6.rc2
- Relax rubygem-ttfunk dep

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 16 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.4.rc2
- Fixed license considering .afm

* Thu May 16 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.3.rc2
- *.ttf fonts and rails.png removal

* Tue Apr 16 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.2.rc2
- Move /data to main package

* Mon Apr 15 2013 Josef Stribny <jstribny@redhat.com> - 1.0.0-0.1.rc2
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to Prawn 1.0.0.rc2

* Tue Dec 04 2012 Josef Stribny <jstribny@redhat.com> - 0.12.0-1
- Initial package
