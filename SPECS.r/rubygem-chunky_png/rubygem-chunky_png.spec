# Generated from chunky_png-1.2.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name chunky_png

Summary: Pure ruby library for read/write, chunk-level access to PNG files
Name: rubygem-%{gem_name}
Version: 1.2.7
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://wiki.github.com/wvanbergen/chunky_png
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch0: rubygem-chunky_png-1.2.7-Fix-Ruby-2.0.0-compatibility.patch
Requires: ruby(release)
Requires: ruby(rubygems)
BuildRequires: ruby
BuildRequires: rubygems-devel
BuildRequires: rubygem(rspec)
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
This pure Ruby library can read and write PNG images without depending on
an external image library, like RMagick. It tries to be memory efficient and
reasonably fast.
It supports reading and writing all PNG variants that are defined in the
specification, with one limitation: only 8-bit color depth is supported. It
supports all transparency, interlacing and filtering options the PNG
specifications allows. It can also read and write textual metadata from PNG
files. Low-level read/write access to PNG chunks is also possible.
This library supports simple drawing on the image canvas and simple operations
like alpha composition and cropping. Finally, it can import from and export to
RMagick for interoperability.


%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
popd

%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/
find %{buildroot} -iname .gitignore -exec rm -f {} \;
find %{buildroot} -iname .yardopts -exec rm -f {} \;
rm -f %{buildroot}%{gem_instdir}/.infinity_test

%check
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i "/require 'bundler\/setup'/ s/^/#/" spec/spec_helper.rb

rspec spec
popd


%files
%dir %{gem_instdir}
%{gem_libdir}
%exclude %{gem_instdir}/.*
%doc %{gem_instdir}/spec
%doc %{gem_instdir}/tasks
%doc %{gem_instdir}/BENCHMARKS.rdoc
%doc %{gem_instdir}/%{gem_name}.gemspec
%doc %{gem_instdir}/benchmarks
%doc %{gem_instdir}/Rakefile
%doc %{gem_instdir}/README.rdoc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/Gemfile
%doc %{gem_docdir}
%exclude %{gem_cache}
%{gem_spec}


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 13 2013 Vít Ondruch <vondruch@redhat.com> - 1.2.7-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to chunky_png 1.2.7.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Vít Ondruch <vondruch@redhat.com> - 1.2.0-4
- Rebuilt for Ruby 1.9.3.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Chris Lalancette <clalance@redhat.com> - 1.2.0-2
- Updates from package review

* Fri Jul 08 2011 Chris Lalancette <clalance@redhat.com> - 1.2.0-1
- Initial package
