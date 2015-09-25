%global	gem_name	json

Name:           rubygem-%{gem_name}
Version:        1.8.2
Release:        102%{?dist}

Summary:        A JSON implementation in Ruby

Group:          Development/Languages

License:        Ruby or GPLv2
URL:            http://json.rubyforge.org
Source0:        http://gems.rubyforge.org/gems/%{gem_name}-%{version}.gem

BuildRequires:	ruby(release)
BuildRequires:	ruby-devel
BuildRequires:  rubygems-devel
BuildRequires:  rubygem(rake)
BuildRequires:	rubygem(minitest4)
BuildRequires:	rubygem(bigdecimal)
BuildRequires:	rubygem(test-unit)

Obsoletes:	rubygem-%{gem_name}-gui < %{version}
Obsoletes:	ruby-%{gem_name}-gui < %{version}
Obsoletes:	ruby-%{gem_name} < %{version}

%description
This is a implementation of the JSON specification according
to RFC 4627 in Ruby.
You can think of it as a low fat alternative to XML,
if you want to store data to disk or transmit it over
a network rather than use a verbose markup language.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation

Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -c -T

# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}

# Change cflags to honor Fedora compiler flags correctly
find . -name extconf.rb | xargs sed -i -e 's|-O3|-O2|' -e 's|-O0|-O2|'

gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec
gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir


%build
%gem_install

find . -name \*gem -exec chmod 0644 {} \;

# compile again
find . -name extconf.rb | while read f
do
	make -C $(dirname $f) clean all install
done

# remove pure
rm -fr .%{gem_instdir}/lib/json/pure*

%install
mkdir -p $RPM_BUILD_ROOT%{gem_dir}
mkdir -p $RPM_BUILD_ROOT%{gem_extdir_mri}
 
cp -a .%{gem_dir}/* %{buildroot}/%{gem_dir}
cp -a .%{gem_extdir_mri}/{gem.build_complete,json} %{buildroot}/%{gem_extdir_mri}/

find $RPM_BUILD_ROOT%{gem_instdir} -name \*.rb -print0 | \
	xargs --null chmod 0644

# We don't need those files anymore.
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/ext
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/install.rb
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/{.require_paths,.gitignore,.travis.yml}
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/lib/json/ext/
rm -rf $RPM_BUILD_ROOT%{gem_instdir}/diagrams
rm -rf $RPM_BUILD_ROOT%{gem_docdir}/rdoc/classes/.src
rm -rf $RPM_BUILD_ROOT%{gem_docdir}/rdoc/classes/.html

rm -rf $RPM_BUILD_ROOT%{gem_instdir}/java/

%check
pushd .%{gem_instdir}
ruby -Ilib:$RPM_BUILD_ROOT%{gem_extdir_mri}:. \
	-e "gem 'minitest', '~> 4' ; Dir.glob('tests/test_*.rb').sort.each {|f| require f}"
popd


%files
%doc %{gem_instdir}/[A-Z]*
%dir %{gem_instdir}
%dir %{gem_libdir}
%dir %{gem_libdir}/%{gem_name}
%{gem_instdir}/tools/
%{gem_libdir}/%{gem_name}.rb
%{gem_libdir}/%{gem_name}/add
%{gem_libdir}/%{gem_name}/common.rb
%{gem_libdir}/%{gem_name}/ext.rb
%{gem_libdir}/%{gem_name}/version.rb
%{gem_libdir}/%{gem_name}/generic_object.rb
%{gem_extdir_mri}/
%{gem_spec}
%exclude %{gem_cache}
%exclude %{gem_instdir}/Rakefile

%files      doc
%{gem_instdir}/Rakefile
%{gem_instdir}/data
%{gem_instdir}/*gemspec
%{gem_docdir}/
%exclude %{gem_instdir}/tests


%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 1.8.2-102
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 16 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.8.2-100
- Update to 1.8.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-104
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.7-103
- Fixes for Ruby 2.1 packaging guidelines (#1107150)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-102
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.7-101
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Josef Stribny <jstribny@redhat.com> - 1.7.7-100
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to JSON 1.7.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Xavier Lamien <laxathom@lxtnow.net> - 1.7.5-1
- Update to Upstream release.
- Add mtasaka changes request.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 21 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.6.5-1
- 1.6.5

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.4.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 18 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.6-1
- Update release.
- Enabled test stage.

* Fri Jun 11 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-3
- Move ruby's site_lib editor to ruby-json-gui.

* Mon May 10 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-2
- Move editor out of ruby-json sub-package.

* Sun May 09 2010 Xavier Lamien <laxathom@fedoraproject.org> - 1.4.3-1
- Update release.
- Split-out json editor.

* Thu Oct 29 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.9-1
- Update release.

* Wed Aug 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-3
- Fix gem scripts and install_dir.
- Enable %%check stage.

* Wed Aug 05 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-2
- Rebuild in correct buildir process.
- Add sub packages.

* Mon Aug 03 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.7-1
- Update release.

* Sat Jun 06 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.6-1
- Update release.

* Tue May 12 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.5-1
- Update release.

* Thu Apr 02 2009 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.4-1
- Update release.

* Sat Jul 12 2008 Xavier Lamien <laxathom@fedoraproject.org> - 1.1.3-1
- Initial RPM release.
