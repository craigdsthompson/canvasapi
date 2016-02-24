from canvas_object import CanvasObject
from util import combine_kwargs


class Course(CanvasObject):

    def conclude(self):
        """
        Marks the course as concluded.

        :calls: `DELETE /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`
        :rtype: bool: True if the course was concluded, False otherwise.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="conclude"
        )
        response_json = response.json()
        return response_json.get('conclude', False)

    def delete(self):
        """
        Permanently deletes the course.

        :calls: `DELETE /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.destroy>`
        :rtype: bool: True if the course was deleted, False otherwise.
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s' % (self.id),
            event="delete"
        )
        response_json = response.json()
        return response_json.get('delete', False)

    def update(self, **kwargs):
        """
        Updates the course.

        :calls: `PUT /api/v1/courses/:id
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.update>`
        :rtype: bool: True if the course was updated, False otherwise.
        """
        try:
            response = self._requester.request(
                'PUT',
                'courses/%s' % (self.id),
                **combine_kwargs(**kwargs)
            )

            super(Course, self).set_attributes(response.json())
            return True
        except Exception:
            return False

    def get_users(self, **kwargs):
        """
        Lists all users in a course. If a filter is provided (`search_term` or
        `enrollment_type`), list only the users that matches the filter.

        :calls: `GET /api/v1/courses/:course_id/users
        <https://canvas.instructure.com/doc/api/courses.html#method.courses.users>`
        :rtype: list: The list of users
        """
        from user import User

        response = self._requester.request(
            'GET',
            'courses/%s/search_users' % (self.id),
            **combine_kwargs(**kwargs)
        )
        return [User(self._requester, user) for user in response.json()]

    def __str__(self):
        return "%s %s %s" % (self.id, self.course_code, self.name)
